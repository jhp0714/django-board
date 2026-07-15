from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from ..forms import QuestionForm
from ..models import Question, Category

@login_required(login_url='common:login')
def question_create(request):
    """
    board 질문 등록
    """
    if request.method == 'POST' :
        selected_category_id = request.POST.get('category')
    else :
        selected_category_id = request.GET.get('category')

    try :
        selected_category_id = int(selected_category_id)
    except (TypeError, ValueError) :
        selected_category_id = None

    if request.method == 'POST' :
        form = QuestionForm(request.POST)

        if form.is_valid() :
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()

            return redirect('board:index', category_name=question.category.name)
    else :
        initial = {}

        if selected_category_id :
            initial['category'] = selected_category_id

        form = QuestionForm(initial=initial)

    categories = Category.objects.all()

    context = {
        'form' : form,
        'categories' : categories,
        'selected_category_id' : selected_category_id,
    }

    return render(request, 'board/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    board 질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('board:detail', question_id=question.id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author =request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)

    categories = Category.objects.all()

    context = {
        'form' : form,
        'categories' : categories,
        'selected_category_id' : question.category_id,
    }

    return render(request, 'board/question_form.html', context)

@login_required(login_url='common:login')
@require_POST
def question_delete(request, question_id):
    """
    board 질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    category_name = question.category.name

    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('board:detail', question_id=question.id)
    question.delete()
    return redirect('board:index', category_name=category_name)