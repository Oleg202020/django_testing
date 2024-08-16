from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):
    NOTE_LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.notes = Note.objects.create(
            title='slug',
            text='Текст',
            slug='not-slug',
            author=cls.author
        )

    def test_notes_list_for_authors(self):
        """Отдельная заметка передаётся на страницу со списком заметок в
        списке object_list в словаре context
        """
        # логинимся в клиенте
        self.client.force_login(self.author)
        # список клиента (автор)
        response = self.client.get(self.NOTE_LIST_URL)
        # Получаем список объектов из словаря контекста.
        object_list = response.context['object_list']
        self.assertTrue((self.notes in object_list))

    def test_notes_list_for_other_users(self):
        """
        В список заметок одного пользователя не попадают
        заметки другого пользователя
        """
        self.client.force_login(self.reader)
        response = self.client.get(self.NOTE_LIST_URL)
        object_list = response.context['object_list']
        self.assertFalse((self.notes in object_list))

    def test_pages_contains_form(self):
        """Проверка передачи формы  на страницы при создании
        и редактировании заметки.
        """
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.notes.slug,)),
        )
        self.client.force_login(self.author)
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIsInstance(response.context['form'], NoteForm)
