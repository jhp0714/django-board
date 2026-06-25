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
    page = request.GET.get('page', 1)
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')

    category = get_object_or_404(Category, name=category_name)

    question_list = (
        Question.objects
        .filter(category=category)
        .select_related('author', 'category')
        .annotate(
            voter_count=Count('voter', distinct=True),
            answer_count=Count('answer', distinct=True),
        )
    )

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    if so == 'recommend':
        question_list = question_list.order_by('-voter_count', '-create_date')
    elif so == 'popular':
        question_list = question_list.order_by('-answer_count', '-create_date')
    elif so == 'hit':
        question_list = question_list.order_by('-hits', '-create_date')
    else:
        question_list = question_list.order_by('-create_date')

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {
        'question_list': page_obj,
        'page': page,
        'kw': kw,
        'so': so,
        'current_category': category,
    }
    return render(request, 'board/question_list.html', context)


def detail(request, question_id):
    """
    board 내용 출력
    """
    question = get_object_or_404(
        Question.objects
        .select_related('author', 'category')
        .prefetch_related('voter', 'comment_set__author'),
        pk=question_id
    )

    question.update_hits()

    page = request.GET.get('page', '1')
    so = request.GET.get('so', 'recent')
    category = question.category

    answer_list = (
        Answer.objects
        .filter(question=question)
        .select_related('author', 'question')
        .prefetch_related('voter', 'comment_set__author')
        .annotate(
            voter_count=Count('voter', distinct=True),
            comment_count=Count('comment', distinct=True),
        )
    )

    if so == 'recommend':
        answer_list = answer_list.order_by('-voter_count', '-create_date')
    elif so == 'popular':
        answer_list = answer_list.order_by('-comment_count', '-create_date')
    else:
        answer_list = answer_list.order_by('-create_date')

    paginator = Paginator(answer_list, 10)
    page_obj = paginator.get_page(page)

    context = {
        'question': question,
        'answer_list': page_obj,
        'page': page,
        'so': so,
        'current_category': category,
    }
    return render(request, 'board/question_detail.html', context)


def redirect_to_question(request):
    """
    board/에 접속하면 기본 게시판으로 리디렉션
    """
    return redirect('board:index', category_name='qna')