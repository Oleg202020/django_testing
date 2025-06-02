from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone
from news.forms import BAD_WORDS
from news.models import Comment, News


@pytest.fixture(autouse=True)
def autouse_db(db):
    pytest.mark.django_db


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(author):
    """Фикстура для создания новости"""
    return News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )


@pytest.fixture
def comment(author, news):
    """создание коментария"""
    return Comment.objects.create(
        text='Текст комментария',
        author=author,
        news=news
    )


@pytest.fixture
def all_news():
    """для проверки пагинации и сортировки новостей"""
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def all_comments(news, author):
    """
    Фикстура для создания нескольких комментариев для
    проверки сортировки комментов
    """
    for index in range(10):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст комментария {index}'
        )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()


@pytest.fixture
def news_home():
    return reverse('news:home')


@pytest.fixture
def news_edit(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def news_delete(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def news_detail(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def users_login():
    return reverse('users:login')


@pytest.fixture
def users_logout():
    return reverse('users:logout')


@pytest.fixture
def users_signup():
    return reverse('users:signup')


@pytest.fixture
def bad_words_data():
    return {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
