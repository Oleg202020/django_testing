from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('notes:add')
        # Создаём пользователя и клиент, логинимся в клиенте.
        cls.user = User.objects.create(username='Крокодил')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {
            'title': 'Заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'}

    def test_user_can_create_note(self):
        """Залогиненный пользователь может создать заметку"""
        # Совершаем запрос через авторизованный клиент.
        response = self.auth_client.post(self.url, data=self.form_data)
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
        self.assertEqual(new_note.author, self.user)

    def test_anonymous_user_cant_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        Note.objects.all().delete()
        # Совершаем запрос от анонимного клиента, в POST-запросе отправляем
        # предварительно подготовленные данные формы с текстом комментария.
        self.client.post(self.url, data=self.form_data)
        # Считаем количество комментариев.
        note_count = Note.objects.count()
        # Ожидаем, что комментариев в базе нет - сравниваем с нулём.
        self.assertEqual(note_count, 0)

    def test_empty_slug(self):
        """
        Если при создании заметки не заполнен slug,
        то он формируется автоматически, с помощью
        функции pytils.translit.slugify.
        """
        self.form_data.pop('slug')
        self.auth_client.post(self.url, data=self.form_data)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)


class TestCommentEditDelete(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаём пользователя - автора комментария.
        cls.author = User.objects.create(username='Автор комментария')
        # Создаём читателя комментария.
        cls.reader = User.objects.create(username='Читатель')
        # Создаём запись в базе данных
        cls.notes = Note.objects.create(title='Заголовок',
                                        text='Текст',
                                        author=cls.author,
                                        slug='new-slug',)
        # Создаём клиент для пользователя-автора и читателя.
        cls.author_client = Client()
        cls.reader_client = Client()
        # "Логиним" пользователя автора и читалтеля в клиенте.
        cls.author_client.force_login(cls.author)
        cls.reader_client.force_login(cls.reader)
        # URL для для добавления комментария.
        cls.url_add = reverse('notes:add')
        # URL для редактирования комментария.
        cls.edit_url = reverse('notes:edit', args=(cls.notes.slug,))
        # URL для удаления комментария.
        cls.delete_url = reverse('notes:delete', args=(cls.notes.slug,))
        # Формируем данные для POST-запроса по обновлению комментария.
        cls.form_data = {
            'title': 'Заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'}

    def test_on_unique_slug(self):
        """Невозможно создать две заметки с одинаковым slug."""
        self.form_data['slug'] = self.notes.slug
        response = self.author_client.post(self.url_add, data=self.form_data)
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(self.notes.slug + WARNING)
        )

    def test_author_can_edit_note(self):
        """Автор может редактировать свои заметки."""
        self.author_client.post(self.edit_url, self.form_data)
        notes_edit = Note.objects.count()
        self.assertEqual(notes_edit, 1)
        new_edit_note = Note.objects.get()
        self.assertEqual(new_edit_note.title, self.form_data['title'])
        self.assertEqual(new_edit_note.text, self.form_data['text'])
        self.assertEqual(new_edit_note.slug, self.form_data['slug'])
        self.assertEqual(new_edit_note.author, self.author)

    def test_other_user_cant_edit_note(self):
        """Читатель не может редактировать чужие заметки."""
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_author_can_delete_note(self):
        """Автор может удалить свои заметки."""
        self.author_client.post(self.delete_url)
        notes_delet = Note.objects.count()
        self.assertEqual(notes_delet, 0)

    def test_other_user_cant_delete_note(self):
        """Читатель не может удалить чужие заметки."""
        self.reader_client.post(self.delete_url)
        notes_not_delet = Note.objects.count()
        self.assertEqual(notes_not_delet, 1)
