from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

NEWS_HOME_URL = pytest.lazy_fixture('news_home')
NEWS_EDIT_URL = pytest.lazy_fixture('news_edit')
NEWS_DELETE_URL = pytest.lazy_fixture('news_delete')
NEWS_DETAIL_URL = pytest.lazy_fixture('news_detail')
USERS_LOGIN_URL = pytest.lazy_fixture('users_login')
USERS_LOGOUT_URL = pytest.lazy_fixture('users_logout')
USERS_SIGNUP_URL = pytest.lazy_fixture('users_signup')
NOT_AUTOR = pytest.lazy_fixture('not_author_client')
ANONIMUS_CLIENT = pytest.lazy_fixture('client')
AUTOR_CLIENT = pytest.lazy_fixture('author_client')


@pytest.mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (NEWS_HOME_URL, ANONIMUS_CLIENT, HTTPStatus.OK),
        (NEWS_DETAIL_URL, ANONIMUS_CLIENT, HTTPStatus.OK),
        (USERS_LOGIN_URL, ANONIMUS_CLIENT, HTTPStatus.OK),
        (USERS_LOGOUT_URL, ANONIMUS_CLIENT, HTTPStatus.OK),
        (USERS_SIGNUP_URL, ANONIMUS_CLIENT, HTTPStatus.OK),
        (NEWS_EDIT_URL, AUTOR_CLIENT, HTTPStatus.OK),
        (NEWS_DELETE_URL, AUTOR_CLIENT, HTTPStatus.OK),
        (NEWS_EDIT_URL, NOT_AUTOR, HTTPStatus.NOT_FOUND),
        (NEWS_DELETE_URL, NOT_AUTOR, HTTPStatus.NOT_FOUND),
    )
)
def test_pages_availability_for_anonymous_user(
    url, parametrized_client, expected_status
):
    """
    Главная страница доступна анонимному пользователю
    Страница отдельной новости доступна анонимному пользователю.
    Страницы регистрации пользователей, входа в учётную запись и
    выхода из неё доступны анонимным пользователям.
    """
    response = parametrized_client.get(url)  # Выполняем запрос.
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (NEWS_EDIT_URL, NEWS_DELETE_URL),
)
def test_redirect_client(url, client, users_login):
    """
    Редирект анонимного пользователя
    будет перенаправлен на страницу логина
    """
    expected_url = f'{users_login}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
