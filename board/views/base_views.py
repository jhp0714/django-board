from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from ..models import Question, Answer, Category
import logging
logger = logging.getLogger('board')

def index(request, category_name='qna'):
    """
    board 목록 출력
    """
    logger.info("INFO 레벨로 출력")
    # 입력 인자
    page = request.GET.get('page', 1)       # 페이지
    kw = request.GET.get('kw', '')          # 검색어
    so = request.GET.get('so', 'recent')    # 정렬 기준

    # 카테고리
    category = get_object_or_404(Category, name=category_name)
    question_list = Question.objects.filter(category=category)

    # 정렬
    if so == 'recommend':
        question_list = question_list.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = question_list.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    elif so == 'hit':
        question_list = question_list.order_by('-hits', '-create_date')
    else:   # recent
        question_list = question_list.order_by('-create_date')

    # 조회
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |                  # 제목 검색
            Q(content__icontains=kw) |                  # 내용 검색
            Q(author__username__icontains=kw) |         # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)   # 답변 글쓴이 검색
        ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {
        'question_list' : page_obj,
        'page': page,
        'kw': kw,
        'so':so,
        'current_category' : category
    }
    return render(request, 'board/question_list.html', context)


def detail(request, question_id):
    """
    board 내용 출력
    """
    question = get_object_or_404(Question, pk = question_id)
    question.update_hits()      # 조회수 업데이트
    page = request.GET.get('page', '1')
    so = request.GET.get('so', 'recent')
    category = question.category

    # 정렬
    if so == 'recommend':
        answer_list = Answer.objects.filter(question=question).annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        answer_list = Answer.objects.filter(question=question).annotate(
            num_answer=Count('comment')).order_by('-num_answer', '-create_date')
    else:   # recent
        answer_list = Answer.objects.filter(question=question).order_by('-create_date')

    # 페이징 처리
    paginator = Paginator(answer_list,10)
    page_obj = paginator.get_page(page)

    context = {
        'question' : question,
        'answer_list':page_obj,
        'page':page,
        'so':so,
        'current_category':category
    }
    return render(request, 'board/question_detail.html', context)

def redirect_to_question(request):
    """
    board/에 접속하면 board/question/으로 리디렉션
    """
    return redirect('board:index', category_name='qna')