<h1 align="center">
    <a href="https://t.me/PrettyAioBot">
        <img alt="pblogo2" src="https://user-images.githubusercontent.com/94391766/231541402-79c0866f-29da-468d-8e54-c68353cf579f.png" width="500"/>
    </a>
</h1>

![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![License](https://img.shields.io/github/license/blago-white/pretty-telegram-bot.svg)
![last commit](https://img.shields.io/github/last-commit/blago-white/pretty-telegram-bot.svg)
![Python ver](https://img.shields.io/badge/python-3.9-green)
![aiogram](https://img.shields.io/badge/aiogram-v2.25-blue)
![psycopg2](https://img.shields.io/badge/psycopg2-v2.9.5-lightgrey)
<br>
<samp>Смотреть примерную структуру приложения можно по этой
    <b>[ссылке](https://www.tldraw.com/r/v2_c_Tv0ABJqq9j5k9m54pkPZ6)</b>
</samp>

<h2 align="center">
    Этот бот найдет тебе новых собесседников в Telegram!
</h2>
Подбор собеседников происходит исходя из <b>трех</b> параметров:
<ul>
    <li><b>Возраст</b></li>
    <li><b>Город</b></li>
    <li><b>Пол</b></li>
</ul>
<p>Эти данные вы указываете при регистрации, поддерживаются все города, правда сейчас только России, вы можете 
настроить параметры как вам угодно<br>
<em>Доступен поиск так же без всяких параметров</em>
</p>

<h2 align="center">Как запустить этот бот?</h2>

<ol>
    <li>
        Через консоль войдите в директорию, в которую собираетесь копировать бота, далее пропишите команду:<br>
        <code> git clone *ссылка на этот репозиторий*</code>
    </li>
    <li>
        После копирования репзитория необходимо обьявить параметры поключения к базе данных <code>PostgreSQL</code>, 
        для этого в файле <code>dbsettings.py</code> вставьте в поля соответствующие значения вашей базы данных
    </li>
    <li>
        Далее необходимо указать токен вашего бота в файле <code>bottoken.py</code>
    </li>
    <li>
        Скачайте все необходимые модули и пакеты, указанные в <code>requirements.txt</code> с помощью 
        <code>pip install -r requirements.txt</code>
    </li>
    <li>
        Для запуска бота через консоль из папки проекта пропишите комманду <code>python prettybot.py</code>, в IDE 
        просто запустите файл <code>prettybot.py</code>
    </li>
</ol>

<p align="center"><b>Готово!</b></p>
