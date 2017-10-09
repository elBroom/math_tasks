from django.utils import timezone

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.utils import override_settings

from math_tasks import settings
from .models import Answer, Task, Tournament, Round


# Create your tests here.
class TasksApiTestCase(TestCase):
    def setUp(self):
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        tournament = Tournament.objects.create(
            title='test',
            is_current=True,
            start_time=start_time,
            end_time=end_time
        )
        self.round = Round.objects.create(
            title='test',
            is_last=False,
            tournament=tournament,
            start_time=start_time,
            end_time=end_time,
        )
        user = User.objects.create_user(username='test', email='test@te.com', password='password', is_staff=True)
        self.password2 = 'password2'
        self.user2 = User.objects.create_user(username='test2', email='test@te.com', password=self.password2)
        self.task1 = Task.objects.create(
            title='Test1',
            text='text1',
            creator=user,
            correct_answer='2.4',
        )
        self.task1.rounds.add(self.round)
        self.task2 = Task.objects.create(
            title='Test2',
            text='text3',
            creator=user,
            correct_answer='x/5',
        )
        self.task2.rounds.add(self.round)

    def test_tournament(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/tournament.html')

    def test_rating(self):
        response = self.client.get('/rating/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/rating.html')

    def test_not_login_tasks(self):
        link = '/tasks/'
        response = self.client.get(link)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '{}?next={}'.format(settings.LOGIN_URL, link))

    def test_not_login_answer(self):
        link = '/answer/{}/'.format(self.task1.id)
        response = self.client.post(link)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '{}?next={}'.format(settings.LOGIN_URL, link))

    def test_method_not_allow_answer(self):
        response = self.client.get('/answer/{}/'.format(self.task1.id))
        self.assertEqual(response.status_code, 405)

    def test_with_login_tasks(self):
        self.client.login(username=self.user2.username, password=self.password2)
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/tasks.html')

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_with_login_answer(self):
        self.client.login(username=self.user2.username, password=self.password2)

        response = self.client.post('/answer/{}/'.format(self.task1.id), {'answer': '2,4'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/tasks/')

        answer = Answer.objects.filter(author=self.user2).filter(task=self.task1).get()
        self.assertEqual(answer.value, '2.4')
        self.assertEqual(answer.is_success, True)

        response = self.client.post('/answer/{}/'.format(self.task2.id), {'answer': 'x / 6'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/tasks/')

        answer = Answer.objects.filter(author=self.user2).filter(task=self.task2).get()
        self.assertEqual(answer.value, 'x/6')
        self.assertEqual(answer.is_success, False)


class UserApiTestCase(TestCase):
    def setUp(self):
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        tournament = Tournament.objects.create(
            title='test',
            is_current=True,
            start_time=start_time,
            end_time=end_time
        )
        self.round = Round.objects.create(
            title='test',
            is_last=True,
            tournament=tournament,
            start_time=start_time,
            end_time=end_time,
        )
        self.password = 'password2'
        self.user = User.objects.create_user(
            username='test', email='test@te.com', password=self.password, is_staff=True)

    def test_login(self):
        self.user.is_staff = False
        self.user.save()
        response = self.client.post(settings.LOGIN_URL, {
            'username': self.user.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)

    def test_register(self):
        response = self.client.post('/register/', {
            'username': 'test3',
            'email': 'test@te.com',
            'password1': 'register',
            'password2': 'register'
        })
        self.assertEqual(response.status_code, 403)
