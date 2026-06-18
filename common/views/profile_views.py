from django.db.models import F, Count
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from itertools import chain
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from board.models import Question, Answer, Comment
from django.http import JsonResponse

import logging

logger = logging.getLogger(__name__)

def profile_base(request, user_id):
    """
    프로필 기본 정보
    """
    user = get_object_or_404(User, pk=user_id)
    context = {'profile_user':user, 'profile_type':'base'}
    return render(request, 'common/profile/profile_base.html', context)

class ProfileObjectListView(ListView):
    """
    프로필 목록 추상 클래스 뷰
    """
    paginate_by = 10  # 한 페이지에 표시할 개수

    def get_queryset(self) :
        self.profile_user = get_object_or_404(User, pk=self.kwargs['user_id'])
        self.so = self.request.GET.get('so', 'recent')
        object_list = self.model.objects.filter(author=self.profile_user)

        if self.so == 'recommend' :
            object_list = object_list.annotate(
                num_voter=Count('voter')).order_by('-num_voter', '-create_date')
        elif self.so == 'popular':
            object_list = object_list.annotate(
                num_answer=Count('answer')).order_by('-num_answer', '-create_date')
        elif self.so == 'hit':
            object_list = object_list.order_by('-hits', '-create_date')
        else :  # recent
            object_list = object_list.order_by('-create_date')

        return object_list

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        paginator = Paginator(self.get_queryset(), self.paginate_by)

        try :
            object_list = paginator.page(page)
        except PageNotAnInteger :
            object_list = paginator.page(1)
        except EmptyPage :
            object_list = paginator.page(paginator.num_pages)

        context.update({
            'profile_user' : self.profile_user,
            'profile_type' : self.profile_type,
            'so' : self.so,
            'object_list' : object_list,
            'page_obj' : object_list,
            'is_paginated' : paginator.num_pages > 1,
        })
        return context

class ProfileQuestionListView(ProfileObjectListView):
    """
    작성한 질문 목록
    """
    model = Question
    template_name = 'common/profile/profile_question.html'
    profile_type = 'question'


class ProfileAnswerListView(ProfileObjectListView):
    """
    작성한 답변 목록
    """
    model = Answer
    template_name = 'common/profile/profile_answer.html'
    profile_type = 'answer'


class ProfileCommentListView(ProfileObjectListView):
    """
    작성한 댓글 목록
    """
    model = Comment
    template_name = 'common/profile/profile_comment.html'
    profile_type = 'comment'

class ProfileVoteListView(ProfileObjectListView):
    """작성한 댓글 목록"""
    template_name = 'common/profile/profile_vote.html'
    profile_type = 'vote'

    def get_queryset(self):
        self.profile_user = get_object_or_404(User, pk=self.kwargs['user_id'])
        question_list = self.profile_user.voter_question.all()
        answer_list = self.profile_user.voter_answer.annotate(category=F('question__category__description'))

        _queryset = sorted(
            chain(question_list, answer_list),
            key = lambda obj: obj.create_date,
            reverse=True
        )
        # 콘솔에 object_list 출력
        # logger.debug(f"ProfileVoteListView queryset: {_queryset}")
        # print(f"ProfileVoteListView queryset1111: {answer_list}")  # 터미널에서 바로 확인용
        return _queryset

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context.update({
            'profile_user' : self.profile_user,
            'profile_type' : self.profile_type,
        })

        # 콘솔에 object_list 출력
        # logger.debug(f"ProfileVoteListView queryset: {context}")
        # print(f"ProfileVoteListView queryset2222: {context}")  # 터미널에서 바로 확인용
        return context