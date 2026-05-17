import sqlite3
import os

# app.py와 경로 계산 방식을 통일: 이 파일 위치(main/) 기준으로 data/ 경로를 구함
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'student.db')


def search_student(name: str) -> list:
    """이름을 기준으로 학생 정보를 조회한다.

    부분 일치 검색을 허용하므로 '김'만 입력해도 김씨 학생 전체가 조회된다.
    SQL Injection 방지를 위해 LIKE 절에 파라미터 바인딩(?)을 사용한다.

    Args:
        name: 검색할 학생 이름 (부분 문자열 가능)

    Returns:
        학생 정보 딕셔너리 리스트. 결과 없으면 빈 리스트.
    """
    # 빈 문자열이면 LIKE '%%'로 전체 DB가 노출되므로 함수 진입 시점에 차단
    if not name or not name.strip():
        return []

    conn = sqlite3.connect(DB_PATH)
    # 컬럼명을 딕셔너리 키로 자동 매핑하기 위해 row_factory 설정
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # LIKE와 % 와일드카드로 부분 일치 검색
    cursor.execute(
        'SELECT * FROM students WHERE name LIKE ?',
        (f'%{name}%',)
    )
    rows = cursor.fetchall()
    conn.close()

    # sqlite3.Row 객체를 일반 딕셔너리로 변환해서 JSON 직렬화가 가능하도록 함
    return [dict(row) for row in rows]
