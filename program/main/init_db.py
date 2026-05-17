import sqlite3
import openpyxl
import os

# 이 파일(init_db.py)이 위치한 main/ 폴더를 기준으로 data/ 경로를 동적으로 계산
# 절대 경로를 사용해야 어느 위치에서 실행해도 경로 오류가 발생하지 않음
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
XLSX_PATH = os.path.join(DATA_DIR, 'student.xlsx')
DB_PATH = os.path.join(DATA_DIR, 'student.db')


def calculate_average(midterm, final):
    """중간고사와 기말고사 점수의 평균을 계산한다."""
    return round((midterm + final) / 2, 1)


def calculate_grade(average):
    """평균 점수를 기준으로 등급을 결정한다.
    A(90+), B(80~89), C(70~79), D(60~69), F(60 미만)
    """
    if average >= 90:
        return 'A'
    elif average >= 80:
        return 'B'
    elif average >= 70:
        return 'C'
    elif average >= 60:
        return 'D'
    else:
        return 'F'


def init_db():
    """student.xlsx 데이터를 읽어 student.db를 초기화한다."""

    # student.xlsx 파일 존재 여부 확인
    if not os.path.exists(XLSX_PATH):
        print(f"오류: {XLSX_PATH} 파일을 찾을 수 없습니다.")
        return

    # openpyxl로 xlsx 파일 읽기 (pandas 미사용, 의존성 최소화)
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb.active

    # DB 연결 (파일이 없으면 자동 생성)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 테이블 생성: 이미 존재하면 건너뜀
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name       TEXT NOT NULL,
            midterm    REAL NOT NULL,
            final      REAL NOT NULL,
            average    REAL NOT NULL,
            grade      TEXT NOT NULL
        )
    ''')

    # xlsx 첫 번째 행은 헤더이므로 건너뜀, 두 번째 행부터 데이터 삽입
    count = 0
    for row in ws.iter_rows(min_row=2, values_only=True):
        student_id, name, midterm, final = row[0], row[1], row[2], row[3]

        # 빈 행 무시
        if student_id is None:
            continue

        avg = calculate_average(float(midterm), float(final))
        grade = calculate_grade(avg)

        # INSERT OR IGNORE: 중복 학번이 있어도 오류 없이 건너뜀
        cursor.execute('''
            INSERT OR IGNORE INTO students (student_id, name, midterm, final, average, grade)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (str(student_id), str(name), float(midterm), float(final), avg, grade))

        if cursor.rowcount > 0:
            count += 1

    conn.commit()
    conn.close()

    print(f"DB 초기화 완료: {count}명의 학생 데이터가 저장되었습니다.")
    print(f"DB 위치: {DB_PATH}")


if __name__ == '__main__':
    init_db()
