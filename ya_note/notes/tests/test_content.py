from django.contrib.auth import get_user_model

from notes.forms import NoteForm
from notes.tests.class_fikst import TestClassContent

User = get_user_model()


class TestContent(TestClassContent):

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
        for name, asert_is in uesers_members:
            self.client.force_login(name)
            with self.subTest(name=name):
                response = self.client.get(self.list_url)
                object_list = response.context['object_list']
                asert_is(self.note, object_list)

    def test_pages_contains_form(self):
        """Проверка передачи формы  на страницы при создании
        и редактировании заметки.
        """
        urls = (
            self.add_url,
            self.edit_url,
        )
        for name in urls:
            with self.subTest(name=name):
                response = self.author_client.get(name)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
