Title: pipenv — как pip, только удобнее
Tags: python, pip, virtualenv, venv, pipenv
Summary: Как пользоваться и в каких случаях стоит обратить внимание на этот инструмент.
Header_cover: /static/swiss_army_knife_darkified.jpg
Status: published

# pipenv

`pipenv` — это замечательный проект, который призван упростить
организацию рабочего процесса для Python-разработчиков. Он
решает несколько наиболее актуальных для разработчика проблем
(да, несколько, вопреки [Unix-way](https://ru.wikipedia.org/wiki/%D0%A4%D0%B8%D0%BB%D0%BE%D1%81%D0%BE%D1%84%D0%B8%D1%8F_Unix)).
Этакий швейцарский нож для питонистов.

`pipenv` нельзя рассматривать как замену `pip`, скорее это надстройка над
`pip`. Но даже
[PyPA всерьёз рекомендует](https://packaging.python.org/guides/tool-recommendations/)
рассмотреть `pipenv` для управления зависимостями приложений, что как
минимум означает, что проект хорошо зарекомендовал себя в сообществе.

Изначальный автор проекта — 
[Кеннет Рейц (Kenneth Reitz)](https://kenreitz.org/) — он ещё
и автор [`requests`](https://github.com/psf/requests) и множества
других проектов "for humans",
очевидно, вдохновлялся пакетными менеджерами из других экосистем,
такими как [`npm`](https://www.npmjs.com/) (JavaScript)
и [`bundler`](https://bundler.io/) (Ruby), так что если вы когда-то
пользовались этими инструментами, то можете заметить множество параллелей.

В названии проекта кроются два основных его назначения:

* `pip` — установка и управления зависимостями проекта;
* `env` — создание и управление виртуальным окружением для проекта.

Грубо говоря, `pipenv` можно рассматривать как симбиоз утилит `pip` и
`venv` (или `virtualenv`), которые работают вместе, пряча многие
неудобные детали от конечного пользователя.

Помимо этого `pipenv` ещё умеет вот такое:

* автоматически находить интерпретатор Python нужной версии
(находит даже интерпретаторы, установленные через
[`pyenv`](https://github.com/pyenv/pyenv)
и [`asdf`](https://asdf-vm.com/)!);
* запускать вспомогательные скрипты для разработки;
* загружать переменные окружения из файла `.env`;
* проверять зависимости на наличие известных уязвимостей.

Стоит сразу оговориться, что если вы разрабатываете библиотеку (или
что-то, что устанавливается через `pip`, и должно работать на нескольких
версиях интерпретатора),
то `pipenv` — не ваш путь. Этот инструмент создан в первую очередь
для разработчиков конечных приложений (консольных утилит, микросервисов,
веб-сервисов). Формат хранения зависимостей подразумевает работу
только на одной конкретной версии интерпретатора (это имеет смысл для
конечных приложений, но для библиотек это, как правило, не приемлемо).
Для разработчиков библиотек существует другой прекрасный инструмент —
[`poetry`](https://python-poetry.org/).

Итак, начнём по порядку.

## Установка

Как я писал в [посте про виртуальные окружения]({filename}virtualenv.md),
не стоит устанавливать пакеты в глобальный интерпретатор, поэтому предпочтительным
способом установки является пакетный менеджер вашей ОС.

Например, на MacOS `pipenv` можно установить через `brew`:

```sh
$ brew install pipenv
```

А на Fedora Linux вот так:

```sh
$ sudo dnf install pipenv
```

На Ubuntu можно установить `pipenv` из [специального PPA](https://launchpad.net/~pypa/+archive/ubuntu/ppa):

```sh
$ sudo apt install software-properties-common python-software-properties
$ sudo add-apt-repository ppa:pypa/ppa
$ sudo apt update
$ sudo apt install pipenv
```

Во всех остальных случаях, в частности на Windows, самый простой способ — это установка
в домашнюю директорию пользователя
(опять же, см. [пост про виртуальные окружения]({filename}virtualenv.md)):

```sh
$ pip install --user pipenv
```

Теперь проверим установку:

```sh
$ pipenv --version
pipenv, version 2018.11.26
```

Если вы получили похожий вывод, значит, всё в порядке.

При возникновении проблем с установкой, обратитесь к
[официальной документации](https://pipenv.pypa.io/en/latest/install/).
Если совсем беда, то напишите комментарий под этим постом,
попробуем помочь 😊

## Файлы `pipenv`

`pipenv` использует свой собственный формат файла для описания зависимостей
проекта — `Pipfile`.
Этот файл имеет [формат TOML](https://github.com/toml-lang/toml).
В принципе его можно редактировать руками, но `pipenv` достаточно неплохо
и сам умеет обновлять этот файл, когда вы просто работаете с утилитой
через командную строку. Структуру этого файла рассмотрим чуть позже.

В паре с `Pipfile` идёт `Pipfile.lock`. Он имеет формат JSON и не
предназначен для редактирования руками. Этот файл хранит контрольные
суммы пакетов, которые вы устанавливаете в проект, что даёт гарантию,
что развёрнутые на разных машинах окружения будут идентичны друг другу.
`pipenv` автоматически обновляет контрольные суммы в этом файле, когда
вы устанавливаете или обновляете зависимости. При развёртывании окружения
`pipenv` сверит сохранённые контрольные суммы с фактически
получившимися, и в случае чего уведомит вас, что развёртывание
не удалось. Это очень важный плюс в копилку `pipenv` по сравнению с `pip`.

Оба этих файла можно и нужно сохранять в системе контроля версий (git).

Вообще, идею использовать два файла для описания зависимостей нельзя
назвать новой.
Здесь явно прослеживается параллель между `Gemfile` и `Gemfile.lock`
из мира Ruby и `package.json` и `package-lock.json` из мира JavaScript.
Все эти файлы имеют схожее назначение.

## Использование

### Инициализация проекта

Давайте создадим простой проект под управлением `pipenv`.

Подготовка:

```sh
$ mkdir pipenv_demo
$ cd pipenv_demo
```

Создать новый проект, использующий конкретную версию Python можно вот такой командой:

```sh
$ pipenv --python 3.8
```

Если же вам не нужно указывать версию так конкретно, то есть шорткаты:

```sh
# Создает проект с Python 3, версию выберет автоматически.
$ pipenv --three

# Аналогично с Python 2.
# В 2020 году эта опция противопоказана.
$ pipenv --two
```

После выполнения одной из этих команд, `pipenv` создал файл `Pipfile` и
виртуальное окружение где-то в заранее определенной директории
(по умолчанию вне директории проекта).

```sh
$ cat Pipfile
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]

[requires]
python_version = "3.8"
```

Это минимальный образец `Pipfile`. В секции `[[source]]` перечисляются
индексы пакетов — сейчас тут только PyPI, но может быть и ваш
собственный индекс пакетов. В секциях `[packages]` и `[dev-packages]`
перечисляются зависимости приложения — те, которые нужны для непосредственной
работы приложения (минимум), и те, которые нужны для разработки (запуск
тестов, линтеры и прочее). В секции `[requires]` указана версия интерпретатора,
на которой данное приложение может работать.

Очень полезно правильно разделять зависимости на "основные" и "разработческие".
Это позволит уменьшить размер окружения при развёртывании на
продакшн (например, размер Docker-образа). Кроме того, чем меньше в системе,
работающей на продакшне, установлено пакетов, тем меньше потенциальных уязвимостей.

Если вам нужно узнать, где именно `pipenv` создал виртуальное окружение
(например, для настройки IDE), то сделать это можно вот так:

```sh
$ pipenv --py
/Users/and-semakin/.local/share/virtualenvs/pipenv_demo-1dgGUSFy/bin/python
```

### Управление зависимостями через `pipenv`

Теперь давайте установим в проект первую зависимость. Делается
это при помощи команды `pipenv install`:

```sh
$ pipenv install requests
```

Давайте посмотрим, что поменялось в `Pipfile` (здесь и дальше я
буду сокращать вывод команд или содержимое файлов при помощи `...`):

```sh
$ cat Pipfile
...

[packages]
requests = "*"

...
```

В секцию `[packages]` добавилась зависимость `requests` с версией `*`
(версия не фиксирована).

А теперь давайте установим зависимость, которая нужна для разработки,
например, восхитительный [линтер `flake8`](https://flake8.pycqa.org/),
передав флаг `--dev` в ту же команду `install`:

```sh
$ pipenv install --dev flake8

$ cat Pipfile
...

[dev-packages]
flake8 = "*"

...
```

Теперь можно увидеть всё дерево зависимостей проекта при помощи команды
`pipenv graph`:

```sh
$ pipenv graph
flake8==3.7.9
  - entrypoints [required: >=0.3.0,<0.4.0, installed: 0.3]
  - mccabe [required: >=0.6.0,<0.7.0, installed: 0.6.1]
  - pycodestyle [required: >=2.5.0,<2.6.0, installed: 2.5.0]
  - pyflakes [required: >=2.1.0,<2.2.0, installed: 2.1.1]
requests==2.23.0
  - certifi [required: >=2017.4.17, installed: 2020.4.5.1]
  - chardet [required: >=3.0.2,<4, installed: 3.0.4]
  - idna [required: >=2.5,<3, installed: 2.9]
  - urllib3 [required: >=1.21.1,<1.26,!=1.25.1,!=1.25.0, installed: 1.25.9]
```

Это бывает полезно, чтобы узнать, что от чего зависит, или почему в вашем
виртуальном окружении есть определённый пакет.

Также, пока мы устанавливали пакеты, `pipenv` создал `Pipfile.lock`,
но этот файл длинный и не интересный, поэтому показывать содержимое я не буду.

Удаление и обновление зависимостей происходит при помощи команд
`pipenv uninstall` и `pipenv update` соответственно. Работают они довольно
интуитивно, но если возникают вопросы, то вы всегда можете получить
справку при помощи флага `--help`:

```sh
$ pipenv uninstall --help
$ pipenv update --help
```

### Управление виртуальными окружениями

Давайте удалим созданное виртуальное окружение:

```sh
$ pipenv --rm
```

И представим себя в роли другого разработчика, который только присоединился
к вашему проекту. Чтобы создать виртуальное окружение и установить
в него зависимости нужно выполнить следующую команду:

```sh
$ pipenv sync --dev
```

Эта команда на основе `Pipfile.lock` воссоздаст точно то же самое виртуальное
окружение, что и у других разработчиков проекта.

Если же вам не нужны dev-зависимости (например, вы разворачиваете ваш
проект на продакшн), то можно не передавать флаг `--dev`:

```sh
$ pipenv sync
```

Чтобы "войти" внутрь виртуального окружения, нужно выполнить:

```sh
$ pipenv shell
(pipenv_demo) $
```

В этом режиме будут доступны все установленные пакеты, а имена `python` и `pip`
будут указывать на соответствующие программы внутри виртуального окружения.

Есть и другой способ запускать что-то внутри виртуального окружения без
создания нового шелла:

```sh
# это запустит REPL внутри виртуального окружения
$ pipenv run python

# а вот так можно запустить какой-нибудь файл
$ pipenv run python script.py

# а так можно получить список пакетов внутри виртуального окружения
$ pipenv run pip freeze
```

### Переменные окружения

Согласно идеологии 12-факторных приложений, конфигурацию принято хранить
отдельно от кода, а [лучше всего конфигурацию вообще
хранить в переменных окружения](https://12factor.net/ru/config)
(environment variables или env vars). Чтобы упростить работу с
переменными окружения в процессе разработки, широкое айти-сообщество придумало
сохранять их в специальный файл `.env` и загружать в шелл по мере
необходимости. Такие файлы используются во множестве фреймворков,
инструментов и экосистем.
`pipenv` упрощает работу с переменными окружения в Python-проектах.

Давайте создадим файл `.env` и запишем туда какое-нибудь значение:

```text
SECRET_VALUE=hello pipenv!
```

**ВАЖНО:** файл `.env` может содержать пароли для подключения к СУБД
или токены для доступа к внешним сервисам. Такие данные **никогда** не должны
попадать в git.

Давайте напишем небольшой скрипт (`script.py`), который будет использовать эту
переменную окружения:

```python
import os

print("Secret value:", os.environ.get("SECRET_VALUE"))
```

Попробуем запустить его без использования `pipenv`:

```sh
$ python script.py
Secret value: None
```

Скрипт вместо секретного значения вывел `None`, потому что переменная
окружения так и осталась просто лежать в файле, и никак не повлияла на
работу скрипта. А теперь запустим этот же скрипт через `pipenv`:

```sh
$ pipenv run python script.py
Loading .env environment variables…
Secret value: hello pipenv!
```

`pipenv` увидел файл `.env` и автоматически загрузил переменные из него.
Скрипт вывел то значение, которое мы и ожидали увидеть. Команда
`pipenv shell` тоже подгружает переменные окружения из файла.

### Запуск скриптов

Часто в процессе разработки встречаются повторяющиеся задачи. Если вы
работаете в команде, то ваши коллеги наверняка тоже с ними сталкиваются.
Было бы разумно сохранить/задокументировать где-то команды, нужные
для решения этих повторяющихся задач, чтобы их было проще найти и чтобы
они всегда выполнялись одинаково. Можно, конечно, использовать обычные
`.sh` файлы, но у `pipenv` тоже есть инструмент, который может в
этом помочь, и даже лучше.

Допустим, что вы регулярно запускаете проверку кода `flake8`, но с
указанием дополнительных флагов, например, вам не нужно проверять
определенную директорию, а так же вы хотите пропускать один вид ошибок
(правильнее было бы просто сохранить эти параметры в конфигурационный файл,
но примера ради будем передавать всё через командную строку):

```sh
$ flake8 --exclude=tests --ignore=E121 .
```

Отредактируем `Pipfile`, создав там секцию `[scripts]` со следующим
содержимым:

```toml
[scripts]
lint = "flake8 --exclude=tests --ignore=E121 ."
```

Теперь тот же самый скрипт можно запустить при помощи команды:

```sh
$ pipenv run lint
```

В качестве бонуса `pipenv` автоматически подгрузит переменные окружения,
так что таким же образом можно выполнять и скрипты, которые зависят от
конфигурации проекта (миграции БД, очистки кэшей, удаление временных файлов,
да что угодно).

## Распространённые проблемы

Перечислю проблемы, с которыми я сталкивался в процессе работы с `pipenv`.

### Лишние зависимости в виртуальном окружении

Бывает, что кроме перечисленных в `Pipfile` и `Pipfile.lock` зависимостей
в виртуальном окружении установлены и другие пакеты. Такое может случиться,
например, при переключении между ветками в git, где в `Pipfile.lock`
находятся разные зависимости. Или, банально, если внутри виртуального
окружения вы установите что-то через `pip` помимо `pipenv`.

Чаще всего вам будет безразлично, есть в виртуальном окружении какие-то
лишние пакеты или нет, но иногда такие лишние пакеты влияют на работу
приложения. Пример из моей практики: [ORM `orator`](https://orator-orm.com/)
будет использовать тот драйвер для подключения к MySQL, [который первым найдёт](
https://github.com/sdispater/orator/blob/0.9/orator/connectors/mysql_connector.py#L7)
в виртуальном окружении, поэтому если вы хотите использовать [`pymysql`](
https://github.com/PyMySQL/PyMySQL),
то нужно убедиться, что в виртуальном окружении нет [`MySQLdb`](
https://github.com/PyMySQL/mysqlclient-python) (он приоритетнее).

Нужно учитывать, что команда `pipenv sync --dev` только доустанавливает пакеты
в виртуальное окружение, но не удаляет оттуда уже установленные. Поэтому, если
вам нужно обеспечить отсутствие в виртуальном окружении лишних пакетов, то
приходится удалять его полностью и создавать заново:

```sh
$ pipenv --rm && pipenv sync --dev
```


### Пререлизные зависимости

По умолчанию `pipenv` игнорирует нестабильные альфа- и бета-версии пакетов,
и устанавливает только стабильные. Может случиться так, что вам нужно
установить пререлизную версию пакета, например, автоформаттер [`black`](
https://github.com/psf/black),
который на данный момент всё ещё не имеет стабильных релизов вообще:

```sh
$ pipenv install --dev black
...
  Hint: try $ pipenv lock --pre if it is a pre-release dependency.
ERROR: ERROR: Could not find a version that matches black
Skipped pre-versions: 18.3a0, 18.3a0, 18.3a1, 18.3a1, 18.3a2, 18.3a2, 18.3a3, 18.3a3, 18.3a4, 18.3a4, 18.4a0, 18.4a0, 18.4a1, 18.4a1, 18.4a2, 18.4a2, 18.4a3, 18.4a3, 18.4a4, 18.4a4, 18.5b0, 18.5b0, 18.5b1, 18.5b1, 18.6b0, 18.6b0, 18.6b1, 18.6b1, 18.6b2, 18.6b2, 18.6b3, 18.6b3, 18.6b4, 18.6b4, 18.9b0, 18.9b0, 19.3b0, 19.3b0, 19.10b0, 19.10b0
There are incompatible versions in the resolved dependencies.
```

Команда завершилась ошибкой, но `pipenv` предлагает воспользоваться опцией
`--pre`, чтобы установить пререлизную зависимость. **Избегайте искушения
сделать так.**

Что произойдёт, если всё-таки рискнуть:

```sh
$ pipenv install --dev --pre black
...
✔ Installation Succeeded
```

На первый взгляд, всё хорошо. Но давайте заглянем в `Pipfile`:

```sh
$ cat Pipfile
...
[pipenv]
allow_prereleases = true
```

Там появилась директива `allow_prereleases = true`, которая глобально меняет
поведение `pipenv` и разрешает ему устанавливать пререлизные версии
вообще любых зависимостей, а не только той, которую вы хотели установить.
Если у вас в `Pipfile` не ограничены версии зависимостей (как у `requests = "*"`),
то следующий запуск `pipenv install` или `pipenv update` может принести
в ваш проект кучу нестабильных зависимостей. Не факт, что приложение
это переживёт.

Чтобы установить пререлизную зависимость правильно, нужно указать
конкретную версию:

```sh
$ pipenv install --dev black==19.10b0
```

Если же вы уже попались в эту ловушку `pipenv`, то просто отредактируйте
`Pipfile` и либо удалите оттуда директиву `allow_prereleases` вообще,
либо поменяйте значение на `false`. После этого можно спать спокойно.


### Мердж-конфликты в `Pipfile.lock`

Когда в двух параллельных ветках происходит установка или обновление
пакетов, либо просто редактируется `Pipfile`, то при слиянии этих веток
обязательно произойдет конфликт в `Pipfile.lock`. Git добавит в этот файл
маркеры конфликтов, после чего, само собой, он перестает быть валидным JSON.
В таких случаях `pipenv` просто превращается в тыкву и ничего не может сделать:

```sh
$ pipenv sync --dev
...
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 3 column 8 (char 24)
```

План выхода из такой ситуации следующий:
1. Не пытайтесь осознанно решать конфликты в `Pipfile.lock` вручную, всё равно
не сможете; `pipenv` сам создал этот файл, вот пусть сам и разбирается.
2. Разрешите конфликт в любую сторону, главное, чтобы в итоге получился
валидный JSON.
3. Пересоздайте `Pipfile.lock` заново:

```sh
$ pipenv lock --keep-outdated
```

Флаг `--keep-outdated` позволяет избежать лишних обновлений версий — вы
ведь просто хотите разрешить конфликты, а не обновить все пакеты, верно?
Тем не менее, `pipenv` может вас проигнорировать, и всё равно обновить
некоторые пакеты, будьте к этому готовы (это [известный баг](https://github.com/pypa/pipenv/issues/3517)).

## Статус проекта: пациент скорее мертв, чем жив, но надежда есть

Стоит отметить, что после [какой-то драмы в сообществе](https://vorpus.org/blog/why-im-not-collaborating-with-kenneth-reitz/),
изначальный автор (Kenneth Reitz) покинул проект (и вообще все свои проекты),
и проект перешёл в общественное достояние.
Любые такие конфликты всегда плохо сказываются на успехе проекта, и `pipenv`,
определенно, переживает сейчас не лучшие времена.
На данный момент последний релиз был 26 ноября 2018 года.
За полтора года накопилось большое количество незарелиженных баг-фиксов,
что говорит о проблемах с поддержкой проекта.

Несмотря на это, я всё равно рекомендую присмотреться к `pipenv`, потому что
он действительно хорош. Недавно проект стал проявлять
[признаки жизни](https://github.com/pypa/pipenv/issues/3369),
и я очень надеюсь, что всё с ним будет хорошо. По-моему, это очень
важный для экосистемы Python проект.

Обновление от 30 мая 2020: `pipenv` наконец выпустил
[долгожданный релиз `2020.5.28`](https://pypi.org/project/pipenv/#history).

Обновляемся:

```sh
$ pip install --user --upgrade pipenv
```

Проект будет жить!

## Заключение

Вместо заключения оставлю вас поразмышлять над вот этой программой:

```python
def use_pipenv():
    know_common_workflows()
    distinguish_between_main_and_dev_dependencies()
    use_dot_env_file()
    use_scripts()
    know_pitfalls()
    print("PROFIT!!!!!")


if work_on_application:
    use_pipenv()
elif work_on_library:
    use_poetry()
else:
    print("wtf")
    use_pip()
```

## Дополнительное чтение

* [Исходный код `pipenv`](https://github.com/pypa/pipenv);
* [Официальная документация](https://pipenv.pypa.io/en/latest/);
* [Гайд на RealPython](https://realpython.com/pipenv-guide/);
* [Kenneth Reitz - Pipenv: The Future of Python Dependency Management - PyCon 2018](https://youtu.be/GBQAKldqgZs);
* [Managing Application Dependencies Tutorial](https://packaging.python.org/tutorials/managing-dependencies/).

## Подпишитесь!

Чтобы получить уведомление о новом посте можно:

* [подписаться на канал в Telegram](https://t.me/pythonic_attacks)
([альтернативная](https://tele.click/pythonic_attacks) [ссылка](https://tele.gg/pythonic_attacks));
* [подписаться на Atom-фид](/feeds/all.atom.xml), если <s>вы олдфаг-старовер</s> вам так удобно.

*Обложка: [James Case, Victorinox Swiss Army Knife](https://commons.wikimedia.org/wiki/File:Victorinox_Swiss_Army_Knife.jpg)*
