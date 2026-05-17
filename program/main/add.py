import openpyxl
import os

# 모든 파일에서 동일한 경로 계산 방식 사용
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(BASE_DIR, '..', 'data', 'student.xlsx')


def calculate_average(midterm: float, final: float) -> float:
    return round((midterm + final) / 2, 1)


def calculate_grade(average: float) -> str:
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
    """새로운 학생 정보를 Excel 파일에 직접 추가한다.

    SQLite 없이 xlsx를 직접 수정하므로
    Excel 파일에서 데이터를 바로 확인할 수 있다.

    Args:
        student_id: 학번
        name: 학생 이름
        midterm: 중간고사 점수 (0~100)
        final: 기말고사 점수 (0~100)

    Returns:
        성공/실패 여부와 메시지를 담은 딕셔너리
    """
    if not (0 <= midterm <= 100 and 0 <= final <= 100):
        return {'success': False, 'message': '점수는 0~100 사이여야 합니다.'}

    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb.active

    # 중복 학번 검사: 추가 전에 전체 데이터를 순회하여 확인
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        if str(row[0]) == str(student_id):
            return {'success': False, 'message': '이미 존재하는 학번입니다.'}

    avg = calculate_average(midterm, final)
    grade = calculate_grade(avg)

    # Excel 마지막 행에 새 데이터 추가 후 저장
    ws.append([student_id, name, midterm, final])
    wb.save(XLSX_PATH)

    return {'success': True, 'message': f'{name} 학생이 성공적으로 추가되었습니다.'}
