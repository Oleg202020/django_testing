from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestClassContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.not_auth_client = User.objects.create(username='Неизвестный')
        cls.author_client = Client()
        cls.reader_client = Client()
        # "Логиним" пользователя автора и читалтеля в клиенте.
        cls.author_client.force_login(cls.author)
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='slug',
            text='Текст',
            slug='not-slug',
            author=cls.author
        )
        cls.form_data = {
            'title': 'Заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'}
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
