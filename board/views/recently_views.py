from ..models import Question, Answer, Comment
from django.views.generic import ListView

class RecentlyObjectListView(ListView):
    """
    최근 목록 추상 클래스 뷰
    """
    limit = 15              # 최근 항목 당 표시할 게시물 개수

    def get_queryset(self):
        object_list = self.model.objects.order_by('-create_date')[:self.limit]
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'recently_type' : self.recently_type,
        })

        return context

class RecentlyQuestionListView(RecentlyObjectListView):
    """
    최근 질문 목록
    """
    model = Question
    template_name = 'common/recently/recently_question.html'
    recently_type = 'question'

class RecentlyAnswerListView(RecentlyObjectListView):
    model = Answer
    template_name = 'common/recently/recently_answer.html'
    recently_type = 'answer'

class RecentlyCommentListView(RecentlyObjectListView):
    model = Comment
    template_name = 'common/recently/recently_comment.html'
    recently_type = 'comment'