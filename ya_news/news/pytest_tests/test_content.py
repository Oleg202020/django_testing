from django.conf import settings

from news.forms import CommentForm


def test_count_on_home_page(client, news_home, all_news):
    """Количество новостей на главной странице — не более 10."""
    response = client.get(news_home)
    object_list = response.context['object_list']
    assert object_list is not None
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_sort_news_on_home_page(client, news_home, all_news):
    """
    Новости отсортированы от самой свежей к самой старой.
    Свежие новости в начале списка.
    """
    response = client.get(news_home)
    object_list = response.context['object_list']
    assert object_list is not None
    all_news_dates = [news.date for news in object_list]
    news_sorted = sorted(all_news_dates, reverse=True)
    assert news_sorted == all_news_dates


def test_note_page_contains_sort_comments(client, all_comments, news_detail):
    """
    Комментарии на странице отдельной новости отсортированы в
    хронологическом порядке: старые в начале списка, новые — в конце.
    """
    response = client.get(news_detail)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_comments = [comment.created for comment in all_comments]
    sorted_comments = sorted(all_comments)
    assert sorted_comments == all_comments


def test_edit_note_page_contains_form(author_client, news_detail):
    """
    авторизованному пользователю доступна форма
    для отправки комментария на странице отдельной новости.
    """
    # Запрашиваем страницу редактирования заметки:
    response = author_client.get(news_detail)
    # Проверяем, есть ли объект form в словаре контекста:
    assert 'form' in response.context
    # Проверяем, что объект формы относится к нужному классу.
    assert isinstance(response.context['form'], CommentForm)


def test_pages_contains_form_for_non_authorize_user(client, news_detail):
    """Анонимному пользователю недоступна форма для отправки комментария"""
    response = client.get(news_detail)
    assert 'form' not in response.context
