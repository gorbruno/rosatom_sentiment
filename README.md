### Как использовать
#### Загрузка файлов проекта
Для начала требуется склонировать репозитории в директорию с проектом:

```bash
cd project_dir

# основной сервер
git  clone https://gitlab.yc.ftc.ru/shift-ml-nlp/sentiment-analyzer/App-Server.git

# ML-сервис
git clone http://gitlab.yc.ftc.ru/shift-ml-nlp/sentiment-analyzer/ml-service.git
```

#### Подготовка к сборке docker-контейнеров
##### Копирование файлов конфигурации

Теперь нужно переместить файлы конфигурации для Docker Compose. Перемещаем файлы docker-compose.yml и .env из директории App-Server в основную директорию проекта, т.е. на уровень выше. В результате основная директория проекта будет выглядеть следующим образом:

__было:__
```
|-project_dir
|   |-App-Server
|   |   |-.env
|   |   |-docker-compose.yml
|   |-ml-service
```
__стало:__

```
|-project_dir
|   |-App-Server
|   |-ml-service
|   |-.env
|   |-docker-compose.yml
```

##### Копирование файлов модели 

Поскольку наша языковая модель довольно большая, а GitLab (и GitHub) не позволяют загружать большие файлы в репозиторий, файлы конфигурации модели и токенайзер потребуется загрузить отдельно. Нужно скачать [эту папку](https://drive.google.com/file/d/1T6T52DT7NqAo8_XBPIU-XthHKv-hsaYi/view?usp=sharing).

После разархивирования скопируйте эту папку в основную директорию ml-сервиса. В результате чего, основная директория проекта будет выглядеть так:

```
|-project_dir
|   |-App-Server
|   |-ml-service
|   |   |-ml_models
|   |-.env
|   |-docker-compose.yml
```

##### Настройка параметров аутентификации в Jira

Основной сервер использует Jira API, соответственно, перед этим происходит процесс аутентификации и в файле конфигурации основного сервера нужно указать свои логин (__JIRA_LOGIN__) и пароль (__JIRA_PASSWORD__). Этот файл называется settings.env и находится он тут:

```
|-project_dir
|   |-App-Server
|   |   |-settings
|   |       |-settings.env 
|   |-ml-service
|   |   |-ml_models
|   |-.env
|   |-docker-compose.yml
```

Также можно указать id задачи в Jira (__JIRA_ISSUE_KEY__), откуда мы хотим получать комментарии.

##### Установка Docker'а

Теперь нужно установить docker. Лучше всего просто установить Docker Desktop, т.к. оно
включает в себя все необходимые инструменты - Docker Compose, Docker Engine и Docker CLI.
Устанавливаем по [этой ссылке](https://docs.docker.com/desktop/?_gl=1*ra15d4*_ga*MTA5MzU4MTk1LjE3MDEwNzU3NjY.*_ga_XJWPQMJYHQ*MTcwNjAwOTA0NS4xNy4xLjE3MDYwMTAwMTAuNTEuMC4w) для вашей ОС.

проверьте установку следующими командами:

```bash
docker --version
# output:
Docker version 24.0.7, build afdd53b
```

```bash
docker-compose --version
# output:
Docker Compose version v2.23.3-desktop.2
```
#### Сборка docker-контейнеров

Переходим в папку с проектом, открываем командную строку и набираем следующую команду:

```bash
docker-compose build
```

Она запустит построение docker-контейнеров и результатом будет мульти-контейнерное приложение, содержащее 4 docker-контейнера: основной сервер, ml-сервис, контейнер с базой данных, клиент для работы с базой данный (__pgadmin__). Эта процедура займёт время, т.к. зависимости довольно тяжёлые, в частности в ml-сервисе используется Pytorch, который также подтягивает зависимости для CUDA и весит это всё довольно прилично. Примерное время от 30 мин.

#### Запуск и использование

Для запуска построенного мульти-контейнерного приложения используем команду:

```bash
docker-compose up
```

Основной Сервер имеет следующие енд-пойнты:

__Анализ комментариев с Jira:__

* URL: http://0.0.0.0:8080/analysis/jira
* HTTP method: __GET__
* response

    ```json
    [
        {
            "message_id": "24540858",
            "publication_date": "2023-12-02T17:29:03.000+0700",
            "user_id": "student_bobrovsky",
            "text": "Сегодня просто чудесный день!",
            "negative_prob": 0.003842093050479889,
            "positive_prob": 0.9801313281059265,
            "neutral_prob": 0.01602652482688427,
            "conclusion": "POSITIVE"
        }
        ...
    ]
    ```

__Анализ текста__

* URL: http://0.0.0.0:8080/analysis/text
* HTTP method: __POST__
* Body:
    ```json
    {
        "text": "Текст для анализа."
    }
    ```
* Response:
    ```json
    {
    "text": "Текст для анализа.",
    "negative_prob": 0.03143327310681343,
    "positive_prob": 0.15019434690475464,
    "neutral_prob": 0.818372368812561,
    "conclusion": "NEUTRAL"
    }
    ```

Можно также делать запросы к ml-сервису отдельно. Он имеет единственный енд-пойнт:

* URL: http://0.0.0.0:8000/analysis
* HTTP method: __POST__
* Body:
    ```json
    {
        "text": "Текст для анализа."
    }
    ```
* Response:
    ```json
    {
    "text": "Текст для анализа.",
    "negative_prob": 0.03143327310681343,
    "positive_prob": 0.15019434690475464,
    "neutral_prob": 0.818372368812561,
    "conclusion": "NEUTRAL"
    }
Аналогично __анализу текста__ от основного сервера.

__Просмотр содержимого базы данных__

Для просмотра содержимого базы данных в проекте поднят контейнер с __pgadmin__. В файле __.env__ указаны e-mail и пароль для входа - __PGADMIN_EMAIL__ и __PGADMIN_PASSWORD__ соответственно (перед построением контейнеров можно указать свои и заходить по ним). Для подключения к базе может потребоваться создать connection. Кликаем правой кнопкой мыши на группу с серверами и нажимает ___Register___->___Server___.

<a href="https://ibb.co/7tMYjXK"><img src="https://i.ibb.co/whG0BR4/pgadmin-instr.png" alt="pgadmin-instr" border="0"></a>

В открывшемся окне вводим название сервера (любое). Далее переходим на вкладку ___Connection___. 

<a href="https://ibb.co/Tr5Kw7V"><img src="https://i.ibb.co/nRS3wYH/pgadmin-instr2.png" alt="pgadmin-instr2" border="0"></a>

В ___Host name___ пишем название сервиса с БД, который указан в файле docker-compose.yml - __db__. Аналогично ___port___ - __5432__, ___maintenance-database___ - дефолтная база данных, которая не имеет практического смысла, но требуется указать __postgres__. ___username___ и ___password___ - значения __DB_USER__ (postgres) и __DB_PASSWORD__ (the_PostGre) соответственно (до построения контейнера можете указать свои в файле ___.env___).

<a href="https://ibb.co/yychkxs"><img src="https://i.ibb.co/YkFDdVj/pgadmin-instr3.png" alt="pgadmin-instr3" border="0"></a>

После успешного подключения можем кидать в нашу БД запросы - кликаем на нашу БД __tone-detector-db__ и нажимаем ___Query Tool___.

<a href="https://ibb.co/SJTSK6s"><img src="https://i.ibb.co/zNcdSmn/pgadmin-instr4.jpg" alt="pgadmin-instr4" border="0"></a>

Далее пишем sql-запросы и запускаем:

<a href="https://ibb.co/c8p15b2"><img src="https://i.ibb.co/s1D2S5s/pgadmin-5.png" alt="pgadmin-5" border="0"></a>

