from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


News_Home_URL = pytest.lazy_fixture('news_home')
News_Edit_URL = pytest.lazy_fixture('news_edit')
News_Delete_URL = pytest.lazy_fixture('news_delete')
News_Detail_URL = pytest.lazy_fixture('news_detail')
Users_Login_URL = pytest.lazy_fixture('users_login')
Users_Logout_URL = pytest.lazy_fixture('users_logout')
Users_Signup_URL = pytest.lazy_fixture('users_signup')
Not_Autor = pytest.lazy_fixture('not_author_client')
Anonimus_Client = pytest.lazy_fixture('client')
Autor_client = pytest.lazy_fixture('author_client')


@pytest.mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (News_Home_URL, Anonimus_Client, HTTPStatus.OK),
        (News_Detail_URL, Anonimus_Client, HTTPStatus.OK),
        (Users_Login_URL, Anonimus_Client, HTTPStatus.OK),
        (Users_Logout_URL, Anonimus_Client, HTTPStatus.OK),
        (Users_Signup_URL, Anonimus_Client, HTTPStatus.OK),
        (News_Edit_URL, Autor_client, HTTPStatus.OK),
        (News_Delete_URL, Autor_client, HTTPStatus.OK),
        (News_Edit_URL, Not_Autor, HTTPStatus.NOT_FOUND),
        (News_Delete_URL, Not_Autor, HTTPStatus.NOT_FOUND),
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
    (News_Edit_URL, News_Delete_URL),
)
def test_redirect_client(url, client, users_login):
    """
    Редирект анонимного пользователя
    будет перенаправлен на страницу логина
    """
    expected_url = f'{users_login}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
