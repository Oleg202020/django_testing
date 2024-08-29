import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import WARNING
from news.models import Comment


NEWS_DETAIL_URL = pytest.lazy_fixture('news_detail')

COMENT_TEXT = 'Новый комментарий.'
NEW_COMENT = {'text': COMENT_TEXT}


def test_anonymous_user_cant_create_comment(client):
    """Анонимный пользователь не может добавить коментарий"""
    comments_before = Comment.objects.count()
    client.post(NEWS_DETAIL_URL, data=NEW_COMENT)
    assert Comment.objects.count() == comments_before


def test_user_can_create_comment(
        author_client,
        news, author,
        news_detail
):
    """Залогиненный пользователь может оставить комментарий"""
    Comment.objects.all().delete()
    response = author_client.post(news_detail, data=NEW_COMENT)
    assertRedirects(response, f'{news_detail}#comments')
    assert Comment.objects.count() == 1
    comment_new = Comment.objects.get()
    assert comment_new.text == COMENT_TEXT
    assert comment_new.news == news
    assert comment_new.author == author


def test_user_cant_use_bad_words(
        author_client,
        news_detail,
        bad_words_data
):
    """
    Проверка на нецензурные слова в коментах,
    невозможно оставить коммент с нецензурными словами
    """
    comments_before = Comment.objects.count()
    response = author_client.post(news_detail, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == comments_before


def test_author_can_edit_comment(
        author_client,
        news_edit,
        comment,
        news_detail
):
    """Авторизованный пользователь может редактировать совой комментарий"""
    comment_old = Comment.objects.get(pk=comment.id)
    #old_news_id = comment.news_id
    response = author_client.post(
        news_edit,
        data=NEW_COMENT
    )
    assertRedirects(response, f'{news_detail}#comments')
    #comment_new = comment.text
    comment_new = Comment.objects.get(pk=comment.id)
    #comment.refresh_from_db()
    #assert comment.news_id == old_news_id
    #assert comment_new != COMENT_TEXT сохранённая переменная до обновления базы
    assert comment_new.author_id == comment_old.author_id
    #assert comment.text == NEW_COMENT['text']  # сохранённая переменная после обновления базы
    assert comment_new.text == NEW_COMENT['text']

def test_author_can_delete_comment(
        author_client,
        news_delete,
        news_detail
):
    """Проверка что автор комментария может удалить совй комментарий"""
    comments_befoere = Comment.objects.count()
    response = author_client.delete(news_delete)
    assertRedirects(response, news_detail + '#comments')
    assert Comment.objects.count() == comments_befoere - 1


def test_user_cant_delete_comment_of_another_user(
        not_author_client, news_delete
):
    """Авторизованный пользователь не может удалять чужой комментарии."""
    comments_before = Comment.objects.count()
    # Выполняем запрос на удаление от пользователя-читателя.
    not_author_client.delete(news_delete)
    assert Comment.objects.count() == comments_before


def test_not_author_cant_edit_comment(
        not_author_client,
        news_edit,
        comment
):
    """Авторизованный пользователь не может редактировать чужие комментарии."""
    comment_old = Comment.objects.get(pk=comment.id)
    #old_text = comment.text
    #old_id_author = comment.author_id
    #old_news_id = comment.news_id
    not_author_client.post(
        news_edit,
        data=NEW_COMENT
    )
    comment_new = Comment.objects.get(pk=comment.id)
    #comment_new = comment.text
    #comment.refresh_from_db()
    assert comment_new.author_id == comment_old.author_id
    assert comment_new.text == comment_old.text
    #assert comment_new == old_text
    #assert comment.text == old_text
    #assert comment.author_id == old_id_author
    #assert comment.news_id == old_news_id
