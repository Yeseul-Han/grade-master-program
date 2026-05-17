from flask import Flask, request, jsonify, render_template
from search import search_student
from add import add_student
import os

# templates/ 폴더가 main/ 밖(프로젝트 루트)에 있으므로 경로를 명시적으로 지정
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
app = Flask(__name__, template_folder=TEMPLATE_DIR)


@app.route('/')
def index():
    """메인 페이지를 렌더링한다."""
    return render_template('index.html')


@app.route('/search')
def search():
    """학생 이름으로 DB를 검색하고 결과를 JSON으로 반환한다.

    Query string 방식: GET /search?name=홍길동
    """
    name = request.args.get('name', '').strip()

    if not name:
        return jsonify({'success': False, 'message': '이름을 입력해주세요.'})

    results = search_student(name)
    return jsonify({'success': True, 'data': results})


@app.route('/add', methods=['POST'])
def add():
    """새로운 학생 정보를 받아 DB에 저장한다.

    Request body (JSON): student_id, name, midterm, final
    """
    data = request.get_json()

    # Content-Type이 application/json이 아니거나 바디가 비어있으면 None 반환됨
    if data is None:
        return jsonify({'success': False, 'message': '요청 형식이 올바르지 않습니다.'})

    # 필수 필드 누락 여부 확인
    required_fields = ['student_id', 'name', 'midterm', 'final']
    for field in required_fields:
        if field not in data or str(data[field]).strip() == '':
            return jsonify({'success': False, 'message': '모든 필드를 입력해주세요.'})

    # 숫자 필드 변환 실패 시 사용자 친화적 오류 반환
    try:
        midterm = float(data['midterm'])
        final = float(data['final'])
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': '점수는 숫자로 입력해주세요.'})

    result = add_student(
        student_id=str(data['student_id']).strip(),
        name=str(data['name']).strip(),
        midterm=midterm,
        final=final
    )
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
