from django.contrib.auth import get_user, get_user_model

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
            (self.author_client, self.assertIn),
            (self.reader_client, self.assertNotIn),
        )
        for user, aserts_is in uesers_members:
            with self.subTest(user=get_user(user), aserts_is=aserts_is):
                response = user.get(self.list_url)
                object_list = response.context['object_list']
                aserts_is(self.note, object_list)

    def test_pages_contains_form(self):
        """Проверка передачи формы  на страницы при создании
        и редактировании заметки.
        """
        urls = (
            self.add_url,
            self.edit_url,
        )
        for url in urls:
            with self.subTest(name=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
