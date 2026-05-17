import sqlite3
import os

# 모든 파일에서 동일한 경로 계산 방식 사용 (일관성 유지)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'student.db')


def calculate_average(midterm: float, final: float) -> float:
    """중간고사와 기말고사의 평균을 소수점 1자리로 반환한다."""
    return round((midterm + final) / 2, 1)


def calculate_grade(average: float) -> str:
    """평균 점수에 따라 등급 문자열을 반환한다.
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


def add_student(student_id: str, name: str, midterm: float, final: float) -> dict:
    """새로운 학생을 DB에 추가한다.

    점수 범위 검사와 중복 학번 검사를 수행하며,
    평균과 등급은 자동으로 계산되어 저장된다.

    Args:
        student_id: 학번 (문자열)
        name: 학생 이름
        midterm: 중간고사 점수 (0~100)
        final: 기말고사 점수 (0~100)

    Returns:
        성공/실패 여부와 메시지를 담은 딕셔너리
    """
    # 점수 범위 유효성 검사: 0~100 벗어나면 DB 저장 전에 차단
    if not (0 <= midterm <= 100 and 0 <= final <= 100):
        return {'success': False, 'message': '점수는 0~100 사이여야 합니다.'}

    avg = calculate_average(midterm, final)
    grade = calculate_grade(avg)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # INSERT OR IGNORE: 중복 학번이면 삽입 자체를 건너뜀 (오류 미발생)
    cursor.execute('''
        INSERT OR IGNORE INTO students (student_id, name, midterm, final, average, grade)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (str(student_id), str(name), float(midterm), float(final), avg, grade))

    conn.commit()

    # rowcount가 0이면 INSERT가 IGNORE된 것 = 중복 학번
    if cursor.rowcount == 0:
        conn.close()
        return {'success': False, 'message': '이미 존재하는 학번입니다.'}

    conn.close()
    return {'success': True, 'message': f'{name} 학생이 성공적으로 추가되었습니다.'}
