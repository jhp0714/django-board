from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from board.models import Category, Question, Answer


class BoardViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='qna',
            description='질문답변',
            has_answer=True,
        )
        self.user = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass1234',
        )
        self.other_user = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass1234',
        )
        self.question = Question.objects.create(
            category=self.category,
            author=self.user,
            subject='테스트 질문',
            content='테스트 내용',
            create_date=timezone.now(),
        )

    def test_question_list_page(self):
        response = self.client.get(
            reverse('board:index', kwargs={'category_name': 'qna'})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 질문')

    def test_question_search(self):
        response = self.client.get(
            reverse('board:index', kwargs={'category_name': 'qna'}),
            {'kw': '테스트'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 질문')

    def test_login_required_for_question_create(self):
        response = self.client.get(reverse('board:question_create'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/common/login/', response.url)

    def test_create_question(self):
        self.client.login(username='user1', password='testpass1234')

        response = self.client.post(
            reverse('board:question_create'),
            {
                'category': self.category.id,
                'subject': '새 질문',
                'content': '새 질문 내용',
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Question.objects.filter(subject='새 질문').exists())

    def test_create_answer(self):
        self.client.login(username='user1', password='testpass1234')

        response = self.client.post(
            reverse('board:answer_create', kwargs={'question_id': self.question.id}),
            {'content': '새 답변 내용'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Answer.objects.filter(content='새 답변 내용').exists())

    def test_question_delete_requires_post(self):
        self.client.login(username='user1', password='testpass1234')

        response = self.client.get(
            reverse('board:question_delete', kwargs={'question_id': self.question.id})
        )

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Question.objects.filter(id=self.question.id).exists())

    def test_other_user_cannot_delete_question(self):
        self.client.login(username='user2', password='testpass1234')

        response = self.client.post(
            reverse('board:question_delete', kwargs={'question_id': self.question.id})
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Question.objects.filter(id=self.question.id).exists())

    def test_vote_question_requires_post(self):
        self.client.login(username='user2', password='testpass1234')

        response = self.client.get(
            reverse('board:vote_question', kwargs={'question_id': self.question.id})
        )

        self.assertEqual(response.status_code, 405)
        self.assertEqual(self.question.voter.count(), 0)

    def test_vote_question(self):
        self.client.login(username='user2', password='testpass1234')

        response = self.client.post(
            reverse('board:vote_question', kwargs={'question_id': self.question.id})
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.question.voter.count(), 1)