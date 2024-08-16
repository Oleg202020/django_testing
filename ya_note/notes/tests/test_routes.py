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

    def test_pages_availability(self):
        """
        Главная страница доступна анонимному пользователю.
        Страницы регистрации пользователей, входа в учётную
        запись и выхода из неё доступны всем пользователям
        """
        urls = (
            ('notes:home', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_diferent_user(self):
        """
        Страницы отдельной заметки, удаления и редактирования
        заметки доступны только автору заметки.
        """
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:edit', 'notes:delete', 'notes:detail'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_auth_users_availabil_pages(self):
        """
        Аутентифицированному пользователю доступна страница
         со списком заметок notes/, страница успешного добавления
         заметки done/, страница добавления новой заметки add/.
        """
        self.client.force_login(self.reader)
        urls = (
            'notes:list',
            'notes:add',
            'notes:success'
        )
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
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
