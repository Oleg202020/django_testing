from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.author_client = Client()
        cls.reader_client = Client()
        # "Логиним" пользователя автора и читалтеля в клиенте.
        cls.author_client.force_login(cls.author)
        cls.reader_client.force_login(cls.reader)
        cls.notes = Note.objects.create(
            title='slug',
            text='Текст',
            slug='not-slug',
            author=cls.author
        )
        cls.list_url = reverse('notes:list', None)

    def test_notes_list_for_authors_and_reader(self):
        """Отдельная заметка передаётся на страницу со списком заметок в
        списке object_list в словаре context
        В список заметок одного пользователя не попадают
        заметки другого пользователя
        """
        uesers_members = (
            (self.author, self.assertIn),
            (self.reader, self.assertNotIn),
        )
        for name, args in uesers_members:
            self.client.force_login(name)
            with self.subTest(name=name):
                response = self.client.get(self.list_url)
                object_list = response.context['object_list']
                args(self.notes, object_list)

    def test_pages_contains_form(self):
        """Проверка передачи формы  на страницы при создании
        и редактировании заметки.
        """
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.notes.slug,)),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
