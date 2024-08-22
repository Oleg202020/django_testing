import pytest
from django.urls import reverse

from news.forms import CommentForm


pytestmark = pytest.mark.django_db


def test_count_on_home_page(client):
    """Количество новостей на главной странице — не более 10."""
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context.get('object_list')
    news_count = object_list.count()
    assert news_count <= 10


def test_sort_news_on_home_page(client):
    """
    Новости отсортированы от самой свежей к самой старой.
    Свежие новости в начале списка.
    """
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context.get('object_list')
    all_news_dates = [news.date for news in object_list]
    news_sorted = sorted(all_news_dates, reverse=True)
    assert news_sorted == all_news_dates


def test_create_note_page_contains_form(client, news):
    """
    Комментарии на странице отдельной новости отсортированы в
    хронологическом порядке: старые в начале списка, новые — в конце.
    """
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_comments = [comment.created for comment in all_comments]
    sorted_comments = sorted(all_comments)
    assert sorted_comments == all_comments


def test_edit_note_page_contains_form(author_client, pk_args):
    """
    авторизованному пользователю доступна форма
    для отправки комментария на странице отдельной новости.
    """
    url = reverse('news:detail', args=pk_args)
    # Запрашиваем страницу редактирования заметки:
    response = author_client.get(url)
    # Проверяем, есть ли объект form в словаре контекста:
    assert 'form' in response.context
    # Проверяем, что объект формы относится к нужному классу.
    assert isinstance(response.context['form'], CommentForm)


def test_pages_contains_form_for_non_authorize_user(client, pk_args):
    """Анонимному пользователю недоступна форма для отправки комментария"""
    url = reverse('news:detail', args=pk_args)
    response = client.get(url)
    assert 'form' not in response.context
