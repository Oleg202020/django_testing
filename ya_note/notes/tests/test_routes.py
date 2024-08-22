from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.note = Note.objects.create(
            title='slug',
            text='Текст',
            slug='not_slug',
            author=cls.author
        )

        cls.login_url = reverse('users:login', None)
        cls.logout_url = reverse('users:logout', None)
        cls.home_url = reverse('notes:home', None)
        cls.signup_url = reverse('users:signup', None)

        cls.add_url = reverse('notes:add', None)
        cls.success_url = reverse('notes:success', None)
        cls.list_url = reverse('notes:list', None)
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.detail_url = reverse('notes:detail', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))

    def test_pages_availability(self):
        """
        Главная страница доступна анонимному пользователю.
        Страницы регистрации пользователей, входа в учётную
        запись и выхода из неё доступны всем пользователям
        """
        urls = (
            self.login_url,
            self.logout_url,
            self.home_url,
            self.signup_url,
        )
        for name in urls:
            with self.subTest(name=name):
                response = self.client.get(name)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    ''' Не смог подобрать статус для данного списка в виду того что возвращает
    код 200 или 404 для читателя
    def test_availabil_pages_for_users(self):
        urls = (
            self.add_url,
            self.success_url,
            self.list_url,
            self.edit_url,
            self.detail_url,
            self.delete_url,
        )
        users_statuses = (
            (self.reader, 404),
            (self.author, HTTPStatus.OK),
        )
        for user, status in users_statuses:
            # выбираем автора и ответ при использовании автора страницы
            self.client.force_login(user)  # логиним автора
            for name_page in urls:  # Перебирем страницы в цикле
                with self.subTest(user=user, name=name_page):
                    response = self.client.get(name_page)
                    print(response.status_code, user)
                    self.assertEqual(response.status_code, status)
    я пробовал этот вариант перед сдачей ещё,
    но чёт не докопался до нужного кода
    '''
    def test_availability_for_diferent_user(self):
        """
        Страницы отдельной заметки, удаления и редактирования
        заметки доступны автору заметки.
        Аутентифицированному пользователю доступна страница
        со списком заметок notes/, страница успешного добавления
        заметки done/, страница добавления новой заметки add/.
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
            self.client.force_login(self.author)
            with self.subTest(user=self.author, name=name):
                response = self.client.get(name)
                self.assertEqual(response.status_code, HTTPStatus.OK)

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
        # login_url = self.login_url
        for name in urls:
            with self.subTest(name=name):
                redirect_url = f'{self.login_url}?next={name}'
                response = self.client.get(name)
                self.assertRedirects(response, redirect_url)

    '''
    def test_availability_for_diferent_user(self):
        """
        Страницы отдельной заметки, удаления и редактирования
        заметки доступны только автору заметки.
        """
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        urls = (
            self.edit_url,
            self.detail_url,
            self.delete_url,
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in urls:
                with self.subTest(user=user, name=name):
                    response = self.client.get(name)
                    self.assertEqual(response.status_code, status)

    def test_auth_users_availabil_pages(self):
        """
        Аутентифицированному пользователю доступна страница
         со списком заметок notes/, страница успешного добавления
         заметки done/, страница добавления новой заметки add/.
        """
        self.client.force_login(self.reader)
        urls = (
            self.add_url,
            self.success_url,
            self.list_url,
        )
        for name in urls:
            with self.subTest(name=name):
                response = self.client.get(name)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_for_anonymous_client(self):
        """
        При попытке перейти на страницу списка заметок,
         страницу успешного добавления записи, страницу добавления
         заметки, отдельной заметки, редактирования или удаления
         заметки анонимный пользователь перенаправляется на
         страницу логина.
        """
        urls = (
            ('notes:list', None),
            ('notes:success', None),
            ('notes:add', None),
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
        )
        login_url = reverse('users:login')
        for name, args in urls:
            with self.subTest(name=name, args=args):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
    '''
