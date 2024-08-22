import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news):
    """Анонимный пользователь не может добавить коментарий"""
    url = reverse('news:detail', args=(news.id,))
    comments_before = Comment.objects.count()
    client.post(url, data={'text': 'Новый комментарий.'})
    assert Comment.objects.count() == comments_before


def test_user_can_create_comment(author_client, news, author):
    """Залогиненный пользователь может оставить комментарий"""
    url = reverse('news:detail', args=(news.id,))
    comments_before = Comment.objects.count()
    response = author_client.post(url, data={'text': 'Новый комментарий.'})
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == comments_before + 1
    comment_new = Comment.objects.get()
    assert comment_new.text == 'Новый комментарий.'
    assert comment_new.news == news
    assert comment_new.author == author


def test_user_cant_use_bad_words(author_client, news):
    """
    Проверка на нецензурные слова в коментах,
    невозможно оставить коммент с нецензурными словами
    """
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_edit_comment(author_client, news, comment):
    """Авторизованный пользователь может редактировать совй комментарий"""
    url_edit = reverse('news:edit', args=(news.id,))
    news_url_detail = reverse('news:detail', args=(comment.id,))
    old_id_author = comment.author_id
    old_news_id = comment.news_id
    response = author_client.post(
        url_edit,
        data={'text': 'Новый комментарий1.'}
    )
    assertRedirects(response, f'{news_url_detail}#comments')
    comment.refresh_from_db()
    assert comment.text == 'Новый комментарий1.'
    assert comment.author_id == old_id_author
    assert comment.news_id == old_news_id


def test_author_can_delete_comment(author_client, news, comment):
    """Проверка что автор комментария может удалить совй комментарий"""
    news_url_detail = reverse('news:detail', args=(comment.id,))
    url_delete = reverse('news:delete', args=(news.id,))
    comments_befoere = Comment.objects.count()
    response = author_client.delete(url_delete)
    assertRedirects(response, news_url_detail + '#comments')
    assert Comment.objects.count() == comments_befoere - 1


def test_user_cant_delete_comment_of_another_user(not_author_client, news):
    """Авторизованный пользователь не может удалять чужой комментарии."""
    url_news_delete = reverse('news:delete', args=(news.id,))
    comments_before = Comment.objects.count()
    # Выполняем запрос на удаление от пользователя-читателя.
    not_author_client.delete(url_news_delete)
    assert Comment.objects.count() == comments_before


def test_not_author_cant_edit_comment(not_author_client, news, comment):
    """Авторизованный пользователь не может редактировать чужие комментарии."""
    url_edit = reverse('news:edit', args=(news.id,))
    old_text = comment.text
    old_id_author = comment.author_id
    old_news_id = comment.news_id
    not_author_client.post(
        url_edit,
        data={'text': 'Новый комментарий1.'}
    )
    comment.refresh_from_db()
    assert comment.text == old_text
    assert comment.author_id == old_id_author
    assert comment.news_id == old_news_id
