# Django Board

Django 기반 게시판 프로젝트입니다. 질문/답변, 댓글, 추천, 카테고리, 검색, 정렬, 조회수, 회원가입/로그인, 소셜 로그인 기능을 포함합니다.

## 주요 기능

- 회원가입 / 로그인 / 로그아웃
- 질문 CRUD
- 답변 CRUD
- 댓글 CRUD
- 질문 / 답변 추천
- 카테고리별 게시글 목록
- 검색
- 최신순 / 추천순 / 인기순 / 조회순 정렬
- 조회수
- 프로필별 작성글 / 댓글 / 추천글 조회

## 기술 스택

- Python
- Django
- SQLite / PostgreSQL
- Bootstrap
- django-allauth
- python-dotenv

## 실행 방법

```bash
git clone https://github.com/jhp0714/django-board.git
cd django-board

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
copy .env.example .env

python manage.py migrate
python manage.py runserver