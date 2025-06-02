from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse
from notes.forms import WARNING
from notes.models import Note
from notes.tests.class_fikst import TestClassContent
from pytils.translit import slugify

User = get_user_model()


class TestContent(TestClassContent):

    def test_user_can_create_note(self):
        """Залогиненный пользователь может создать заметку"""
        Note.objects.all().delete()
        # Совершаем запрос через авторизованный клиент.
        response = self.author_client.post(self.add_url, data=self.form_data)
        # Проверяем, что редирект привёл на страницу успешной записи
        self.assertRedirects(response, reverse('notes:success'))
        # Считаем количество комментариев.
        notes_coment = Note.objects.count()
        # Убеждаемся, что есть одина запись.
        self.assertEqual(notes_coment, 1)
        # Получаем объект записи из базы.
        new_note = Note.objects.get()
        # Проверяем, что все атрибуты комментария совпадают с ожидаемыми.
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_anonym_user_cant_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        notes_before = Note.objects.count()
        # Совершаем запрос от анонимного клиента, в POST-запросе отправляем
        # предварительно подготовленные данные формы с текстом комментария.
        self.client.post(self.add_url, data=self.form_data)
        # Считаем количество комментариев.
        note_count = Note.objects.count()
        # Ожидаем, что комментариев в базе нет - сравниваем с нулём.
        self.assertEqual(note_count, notes_before)

    def test_empty_slug(self):
        """
        Если при создании заметки не заполнен slug,
        то он формируется автоматически, с помощью
        функции pytils.translit.slugify.
        """
        Note.objects.all().delete()
        self.form_data.pop('slug')
        self.author_client.post(self.add_url, data=self.form_data)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_on_unique_slug(self):
        """Невозможно создать две заметки с одинаковым slug."""
        notes_before = Note.objects.count()
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(self.add_url, data=self.form_data)
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        note_count = Note.objects.count()
        self.assertEqual(note_count, notes_before)

    def test_author_can_edit_note(self):
        """Автор может редактировать свои заметки."""
        self.author_client.post(self.edit_url, self.form_data)
        new_edit_note = Note.objects.get(id=self.note.id)
        self.assertEqual(new_edit_note.title, self.form_data['title'])
        self.assertEqual(new_edit_note.text, self.form_data['text'])
        self.assertEqual(new_edit_note.slug, self.form_data['slug'])
        self.assertEqual(new_edit_note.author, self.note.author)

    def test_other_user_cant_edit_note(self):
        """Читатель не может редактировать чужие заметки."""
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_db.title)
        self.assertEqual(self.note.text, note_db.text)
        self.assertEqual(self.note.slug, note_db.slug)
        self.assertEqual(self.note.author, note_db.author)

    def test_author_can_delete_note(self):
        """Автор может удалить свои заметки."""
        notes_before = Note.objects.count()
        self.author_client.post(self.delete_url)
        notes_delet = Note.objects.count()
        self.assertEqual(notes_delet, notes_before - 1)

    def test_other_user_cant_delete_note(self):
        """Читатель не может удалить чужие заметки."""
        notes_in_bd = Note.objects.count()
        self.reader_client.post(self.delete_url)
        notes_not_delet = Note.objects.count()
        self.assertEqual(notes_not_delet, notes_in_bd)
