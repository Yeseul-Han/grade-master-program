# 학생 성적 관리 프로그램 (Excel 직접 관리 버전)

Flask 기반 웹 애플리케이션으로, 학생 성적을 조회하고 관리하는 교내 임직원용 프로그램입니다.

> **브랜치 안내**
> - `master` : SQLite DB를 사용하는 원본 버전
> - `excel-version` : Excel 파일을 직접 읽고 쓰는 현재 버전 (별도 DB 불필요)

## master 버전과의 차이점

| 항목 | master (SQLite) | excel-version (현재) |
|------|----------------|----------------------|
| 데이터 저장소 | `student.db` (별도 DB 파일) | `student.xlsx` 하나로 관리 |
| 초기 설정 | `python init_db.py` 실행 필요 | 없음 |
| 데이터 확인 방법 | DB 뷰어 또는 `check_db.py` | Excel 파일을 열면 바로 확인 |
| 포함 파일 | `init_db.py`, `check_db.py` 포함 | 두 파일 없음 |
| 서버 실행 단계 | 2단계 (init → app 실행) | 1단계 (app만 실행) |

## 주요 기능

- **학생 검색**: 이름 기준 부분 일치 검색, 학번/점수/평균/등급 조회
- **학생 추가**: 학번·이름·중간고사·기말고사 입력 시 평균과 등급 자동 계산 후 Excel에 저장

## 기술 스택

| 구분 | 기술 |
|------|------|
| Frontend | HTML, CSS, JavaScript (fetch API) |
| Backend | Python, Flask |
| 데이터 저장 | Excel (openpyxl) |

## 프로젝트 구조

```
program/
├── data/
│   └── student.xlsx       # 데이터 원본이자 저장소 (Excel로 직접 확인/편집 가능)
├── main/
│   ├── search.py          # 학생 검색 기능 (xlsx 직접 읽기)
│   ├── add.py             # 학생 추가 및 점수 계산 (xlsx 직접 쓰기)
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

### 2. 서버 실행

```bash
cd program/main
python app.py
```

### 3. 브라우저 접속

```
http://localhost:5000
```

> `student.xlsx`에 데이터가 미리 있으면 바로 검색이 가능합니다.
> 학생을 추가하면 `student.xlsx`에 즉시 반영되므로 Excel을 열어 확인할 수 있습니다.

## API 명세

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/` | 메인 페이지 |
| GET | `/search?name=이름` | 학생 검색 |
| POST | `/add` | 학생 추가 |
