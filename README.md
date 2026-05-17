# 학생 성적 관리 프로그램

Flask 기반 웹 애플리케이션으로, 학생 성적을 조회하고 관리하는 교내 임직원용 프로그램입니다.

## 주요 기능

- **학생 검색**: 이름 기준 부분 일치 검색, 학번/점수/평균/등급 조회
- **학생 추가**: 학번·이름·중간고사·기말고사 입력 시 평균과 등급 자동 계산 후 저장

## 기술 스택

| 구분 | 기술 |
|------|------|
| Frontend | HTML, CSS, JavaScript (fetch API) |
| Backend | Python, Flask |
| Database | SQLite3 |

## 프로젝트 구조

```
program/
├── data/
│   └── student.xlsx       # 원본 학생 데이터
├── main/
│   ├── init_db.py         # DB 초기화 (xlsx → student.db 변환)
│   ├── check_db.py        # DB 내용 확인 (디버깅용)
│   ├── search.py          # 학생 검색 기능
│   ├── add.py             # 학생 추가 및 점수 계산
│   └── app.py             # Flask 서버 및 라우팅
└── templates/
    └── index.html         # 웹 UI
```

## 등급 기준

| 평균 점수 | 등급 |
|----------|------|
| 90점 이상 | A |
| 80 ~ 89점 | B |
| 70 ~ 79점 | C |
| 60 ~ 69점 | D |
| 60점 미만 | F |

## 실행 방법

### 1. 의존성 설치

```bash
pip install flask openpyxl
```

### 2. DB 초기화 (최초 1회)

```bash
cd program/main
python init_db.py
```

### 3. 서버 실행

```bash
python app.py
```

### 4. 브라우저 접속

```
http://localhost:5000
```

## API 명세

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/` | 메인 페이지 |
| GET | `/search?name=이름` | 학생 검색 |
| POST | `/add` | 학생 추가 |
