# Тестовое задание для компании  [Royal Ark](https://royalarkgames.com/)
[Файл с тестовым заданием](https://github.com/evergreenacorn/RA_TEST_TASK_flask-pandas-dash-pg-docker/blob/master/app/task_data/Тестовое%20задание%20Python%20developer.pdf)

### Что сделал
Согласно заданию:
1. Разработал приложение, включающее:
   - возможность импорта csv-файлов
   - возможность вывода отчета в виде таблицы
   - возможность фильтрации данных
2. Спроектировал базу данных приложения, включающую таблицы:
   - Event(событие)
   - EventType(тип события)
   - MediaSource(медиа ресурс)
   - Company(компания)
   - Platform(платформа)
3. Приложение, построено на базе микро-фреймворка flask
4. Интерактивная таблица, описана на backend стороне с помощью библиотеки dash, что позволяет исключить все сложности написания frontend части приложения
5. docker'изация, позволяющая быстро развернуть тестовый стенд приложения и включающая возможность удаленной отладки контейнера

### Как запускать:
После первого запуска `docker-compose up` из папки с проектом запустить команду:
- ```docker exec testtaskflask_app bash -c "flask db init && flask db migrate && flask db upgrade"```

После запуска перейти по:
- http://127.0.0.1:5000/

### Sitemap
|Описание|Путь|
|---|---|
|домашняя страница|/index|
|страница импорта csv-файлов|/import_csv|
|отчет в виде таблицы с функциональными фильтрами|/dashboard|

### TODO:
- Сделать reusable-запрос таблицы(соглано dry)
- Упростить helper-классы импорта, объединив в один
- Добавить тесты
- Поправить верстку
