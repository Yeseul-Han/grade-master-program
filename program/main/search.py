import openpyxl
import os

# 이 파일(search.py)이 위치한 main/ 폴더를 기준으로 xlsx 경로를 계산
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(BASE_DIR, '..', 'data', 'student.xlsx')


def calculate_average(midterm, final):
    return round((float(midterm) + float(final)) / 2, 1)


def calculate_grade(average):
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


def search_student(name: str) -> list:
    """이름 기준으로 Excel에서 학생을 검색한다.

    SQLite 없이 xlsx 파일을 직접 읽으므로
    init_db.py 실행 없이 바로 사용 가능하다.

    Args:
        name: 검색할 이름 (부분 일치 허용)

    Returns:
        학생 정보 딕셔너리 리스트. 결과 없으면 빈 리스트.
    """
    # 빈 문자열로 전체 데이터가 노출되는 것을 방지
    if not name or not name.strip():
        return []

    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb.active

    results = []
    # 첫 번째 행은 헤더이므로 두 번째 행부터 읽기
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue

        student_id, sname, midterm, final = row[0], row[1], row[2], row[3]

        # 대소문자 구분 없이 부분 일치 검색
        if name.strip().lower() in str(sname).lower():
            avg = calculate_average(midterm, final)
            grade = calculate_grade(avg)
            results.append({
                'student_id': str(student_id),
                'name':       str(sname),
                'midterm':    float(midterm),
                'final':      float(final),
                'average':    avg,
                'grade':      grade
            })

    return results
