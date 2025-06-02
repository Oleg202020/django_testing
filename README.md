# Тестирование Django‑проектов &laquo;Ya News&raquo; и &laquo;Ya Note&raquo;

Этот репозиторий объединяет **автоматические тесты** для двух учебных Django‑приложений:
Цель репозитория — показать, как организовать тесты на двух популярных фреймворках


|   Проект  |          Назначение            |      Директория тестов     |         Фреймворк          |
|-----------|--------------------------------|----------------------------|----------------------------|
|**ya_news**| новостной сайт с комментариями |`ya_news/news/pytest_tests/`| `pytest + pytest‑django`   |
|**ya_note**| сервис личных заметок          |`ya_note/notes/tests/`      |`unittest (Django TestCase)`|


**Почему два фреймворка?**  
*Pytest* позволяет писать лаконичные, параметризованные тесты на &laquo;Ya News&raquo;,  
тогда как стандартный *unittest* остаётся встроенной частью Django и применяется в &laquo;Ya Note&raquo;. 
Сравнение подходов в живом коде — лучший способ увидеть их сильные и слабые стороны.

---

## 📑 Содержание

- [Структура репозитория](#1-структура-репозитория)
- [Быстрый старт](#2-быстрый-старт)
- [Запуск тестов выборочно](#3-запуск-тестов-выборочно)
- [Особенности тестов «Ya News»](#4-особенности-тестов-ya-news)
- [Особенности тестов «Ya Note»](#5-особенности-тестов-ya-note)
- [Дополнительные команды разработки](#6-дополнительные-команды-разработки)
- [Требуемые версии](#7-требуемые-версии)
- [Контакты](#контакты)

---

## 1. Структура репозитория

```
Dev
 └── django_testing
     ├── ya_news
     │   ├── news
     │   │   ├── fixtures/
     │   │   ├── migrations/
     │   │   ├── pytest_tests/   <- Директория с тестами pytest для проекта ya_news
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanews/
     │   ├── manage.py
     │   └── pytest.ini
     ├── ya_note
     │   ├── notes
     │   │   ├── migrations/
     │   │   ├── tests/          <- Директория с тестами unittest для проекта ya_note
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanote/
     │   ├── manage.py
     │   └── pytest.ini
     ├── .gitignore
     ├── README.md
     ├── requirements.txt
     └── structure_test.py
```

## 2. Быстрый старт

```bash
git clone git@github.com:Oleg202020/django_testing.git
cd django_testing

python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

pip install -r requirements.txt

bash run_tests.sh               # запустит ВСЕ тесты
```
Скрипт:
* 1 применит миграции к временной БД;
* 2 выполнит pytest‑тесты проекта «Ya News»;
* 3 выполнит unittest‑тесты проекта «Ya Note»;
* 4 выведет суммарный отчёт.
Зелёные проверки — тесты пройдены ✅

## 3. Запуск тестов выборочно

```bash
# Только pytest‑тесты &laquo;Ya News&raquo;
pytest ya_news

# Только unittest‑тесты &laquo;Ya Note&raquo;
python ya_note/manage.py test notes
```

---

## 4. Особенности тестов «Ya News»

* **Фикстуры находятся** в ya_news/news/pytest_tests/conftest.py
(создание пользователей, новостей, комментариев, url‑reverse и т.п.).

* **Покрываемые сценарии:**
    * пагинация главной страницы;
    * сортировка новостей и комментариев;
    * фильтрация непристойной лексики при помощи BAD_WORDS;
    * доступность CRUD‑операций для разных ролей (автор, не автор, аноним).

* **Полезные команды:**
    * pytest -q — лаконичный вывод,
    * pytest -vv — подробный вывод с именами тестов,
    * pytest --lf — только упавшие ранее тесты.

---

## 5. Особенности тестов «Ya Note»
* Тесты расположены в ya_note/notes/tests/ и наследуются от django.test.TestCase.
* Используются параметры:
    * setUpTestData — быстрая фикстура на весь класс;
    * force_login для имитации авторизации;
    * подробные проверки CRUD‑прав для заметок.

---

## 6. Дополнительные команды разработки

|  Задача	                   |  Команда                              |
|------------------------------|---------------------------------------|
|Запустить сервер Ya News      |	python ya_news/manage.py runserver |
|Запустить сервер Ya Note      |	python ya_note/manage.py runserver |
|Обновить список зависимостей  |	pip freeze > requirements.txt      |
|Проверить стиль	flake8     |                                       |


## 7. Требуемые версии
|Пакет	        | Версия  |
|---------------|---------|
|Python	        |3.10 +   |
|Django	        |4.2.x    |
|pytest	        |8.x      |
|pytest‑django	|4.x      |
|coverage	    |7.x      |

Точные версии закреплены в 'requirements.txt'.

*Удачного тестирования 🚀*

---

## Контакты

* Автор: Larionov Oleg
* E-mail: jktu2005@yandex.ru
* GitHub: @Oleg202020
