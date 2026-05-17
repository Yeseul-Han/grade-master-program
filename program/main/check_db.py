import sqlite3
import os

# init_db.py와 동일한 경로 계산 방식 사용 (일관성 유지)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'student.db')


def check_db():
    """DB에 저장된 모든 학생 정보를 콘솔에 출력한다. (개발/디버깅 전용)"""

    if not os.path.exists(DB_PATH):
        print("오류: student.db 파일이 없습니다. init_db.py를 먼저 실행하세요.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()

    conn.close()

    # 헤더 출력
    print("-" * 65)
    print(f"{'학번':<12} {'이름':<8} {'중간고사':>6} {'기말고사':>6} {'평균':>6} {'등급':>4}")
    print("-" * 65)

    for row in rows:
        student_id, name, midterm, final, average, grade = row
        print(f"{student_id:<12} {name:<8} {midterm:>6.1f} {final:>6.1f} {average:>6.1f} {grade:>4}")

    print("-" * 65)
    print(f"총 학생 수: {len(rows)}명")


if __name__ == '__main__':
    check_db()
