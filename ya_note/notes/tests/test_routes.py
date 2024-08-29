from http import HTTPStatus

from django.contrib.auth import get_user_model

from notes.tests.class_fikst import TestClassContent

User = get_user_model()


class TestRoutes(TestClassContent):

    def test_availabil_pages_for_users(self):
        """Страницы отдельной заметки, удаления и редактирования
        заметки доступны только автору заметки.
        Аутентифицированному пользователю доступна страница
        со списком заметок notes/, страница успешного добавления
        заметки done/, страница добавления новой заметки add/.
        """
        urls = (
            # доступно для всех
            (self.login_url, self.not_auth_client, HTTPStatus.OK),
            (self.logout_url, self.not_auth_client, HTTPStatus.OK),
            (self.home_url, self.not_auth_client, HTTPStatus.OK),
            (self.signup_url, self.not_auth_client, HTTPStatus.OK),
            # ----------------------читатель
            (self.add_url, self.author, HTTPStatus.OK),
            (self.success_url, self.author, HTTPStatus.OK),
            (self.list_url, self.author, HTTPStatus.OK),
            # -------------------- только афтор
            (self.edit_url, self.author, HTTPStatus.OK),
            (self.detail_url, self.author, HTTPStatus.OK),
            (self.delete_url, self.author, HTTPStatus.OK),
            # --------------------------читателю не доступно
            (self.edit_url, self.reader, HTTPStatus.NOT_FOUND),
            (self.detail_url, self.reader, HTTPStatus.NOT_FOUND),
            (self.delete_url, self.reader, HTTPStatus.NOT_FOUND),
        )
        for name_page, user, status in urls:
            # выбираем автора и ответ при использовании автора страницы
            self.client.force_login(user)  # логиним автора
            with self.subTest(user=user, name=name_page, status=status):
                response = self.client.get(name_page)
                self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        """
        При попытке перейти на страницу списка заметок,
         страницу успешного добавления записи, страницу добавления
         заметки, отдельной заметки, редактирования или удаления
         заметки анонимный пользователь перенаправляется на
         страницу логина.
        """
        urls = (
            self.add_url,
            self.success_url,
            self.list_url,
            self.edit_url,
            self.detail_url,
            self.delete_url,
        )
        for name in urls:
            with self.subTest(name=name):
                redirect_url = f'{self.login_url}?next={name}'
                response = self.client.get(name)
                self.assertRedirects(response, redirect_url)
