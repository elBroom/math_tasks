from django.utils import timezone

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Article
from tasks.models import Tournament, Round


# Create your tests here.
class NewsApiTestCase(TestCase):
    def setUp(self):
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        tournament = Tournament.objects.create(
            title='test',
            is_current=True,
            start_time=start_time,
            end_time=end_time
        )
        Round.objects.create(
            title='test',
            is_last=False,
            tournament=tournament,
            start_time=start_time,
            end_time=end_time,
        )
        user = User.objects.create_user(username='test', email="test@te.com", password='password', is_staff=True)
        self.article1 = Article.objects.create(
            title='Test1',
            text = 'text1',
            author=user,
            is_public=True
        )
        self.article2 = Article.objects.create(
            title='Test2',
            text='text2',
            author=user,
            is_public=False
        )

    def test_list(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/list.html')

    def test_item(self):
        response = self.client.get('/news/{}/'.format(self.article1.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/item.html')

    def test_not_found(self):
        response = self.client.get('/news/{}/'.format(self.article2.id))
        self.assertEqual(response.status_code, 404)
