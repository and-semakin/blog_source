Title: Линтеры в Python
Tags: python, flake8, pylint
Summary: Обзор популярных статических анализаторов для Python-кода и как они экономят разработчику один день жизни в месяц.
Header_cover: /static/traffic_lights.jpg
Status: published

# Линтеры

В сообществе Python, как и в любой другой группе людей, существует некое
коллективное знание. Множество людей прошлось по всем возможным граблям
и получило опыт через набитые шишки. Затем через какое-то время,
благодаря выступлениям на конференциях, официальным заявлениям,
документам, статьям в блогах, код-ревью и личному общению,
это знание стало коллективным. Теперь мы просто называем его
“хорошими практиками”.

К таким хорошим практикам можно отнести, например, следующие.

* Форматировать код по [PEP8](https://www.python.org/dev/peps/pep-0008/)
— если этого не делать, то другим людям будет намного сложнее понимать
ваш код; в плохо оформленном коде сложнее увидеть суть,
потому что мозг постоянно отвлекается на не несущие смысловой нагрузки
особенности оформления.
* Не допускать объявленных, но неиспользуемых переменных/функций/импортов
— опять же, это усложняет восприятие кода; читателю потребуется потратить
время на то, чтобы осознать, что вот на эту сущность обращать внимания не
нужно.
* Писать короткие функции — слишком сложные функции с большим
количеством ветвлений и циклов тяжело понимать.
* Не использовать изменяемый объект в качестве значения аргумента
функции по умолчанию — иначе в результате можно получить
[очень неожиданные эффекты](https://docs.python-guide.org/writing/gotchas/#mutable-default-arguments).

Соблюдать (и даже просто помнить) все хорошие практики — не самая простая
задача. Зачастую люди плохо справляются с тем, чтобы отсчитывать пробелы
и контролировать переменные, и вообще склонны допускать ошибки по
невнимательности. Таковы люди, ничего не поделаешь. Машины, наоборот,
прекрасно справляются с такими хорошо определёнными задачами, поэтому
появились инструменты, которые контролируют следование хорошим практикам.

В компилируемых языках ещё на этапе компиляции программист может получить
<s>по щщам</s> первый полезный фидбэк о написанном коде.
Компилятор проверит, что код валиден и может быть скомпилирован, а также может
выдать предупреждения и рекомендации, как сделать код лучше или читаемее.
Т.к. Python является интерпретируемым языком, где этап компиляции как таковой
отсутствует, линтеры особенно полезны. На самом деле, это очень важно и
круто — узнать, что твой код как минимум является валидным Python-кодом,
даже не запуская его.

В этом посте я рассмотрю два самых популярных линтера для Python:

* [flake8](https://flake8.pycqa.org/en/latest/);
* [pylint](https://www.pylint.org/).

> Термин “lint” впервые начал использоваться в таком значении в 1979 году.
> Так называлась программа для статического анализа кода на C,
> которая предупреждала об использовании непортабельных на другие архитектуры
> языковых конструкций. С тех пор “линтерами” называют любые статические
> анализаторы кода, которые помогают находить распространённые ошибки, делать
> его однообразным и более читаемым. А названо оно "lint" в честь вот такой
> штуки:

![lint roller]({static}/static/lint_roller.jpg)


## flake8

`flake8` — это утилита-комбайн, которая органично объединяет в себе несколько
других анализаторов кода (`pycodestyle`, `pyflakes` и `mccabe`), а также
имеет огромную экосистему плагинов, которые могут добавить к стандартной
поставке ещё кучу различных проверок. На данный момент, это самый
популярный линтер для Python-кода. Кроме того, он предельно прост в
настройке и использовании.

### Установка

`flake8` устанавливается, как и любой другой Python-пакет,
через `pip`. **Внутри виртуального окружения** проекта выполните:

```sh
$ pip install flake8
```

Если вы пользуетесь `pipenv`, то `flake8` нужно устанавливать
как dev-зависимость (ведь для работы программы линтер не нужен,
он нужен только для разработчика):

```sh
$ pipenv install --dev flake8
```

Аналогично с `poetry`:

```sh
$ poetry add --dev flake8
```

Проверим установку:

```sh
$ flake8 --version
3.8.1 (mccabe: 0.6.1, pycodestyle: 2.6.0, pyflakes: 2.2.0) CPython 3.8.2 on Linux
```


### Использование

Для работы `flake8` нужно просто указать файл или директорию, которые
нужно проверять, например:

```sh
# проверить один файл
$ flake8 file.py

# проверить директорию рекурсивно 
$ flake8 src/

# проверить текущую директорию рекурсивно
$ flake8 .
```

Давайте для демонстрации попытаемся написать программу с как можно большим
количеством “плохих практик”:

<script src="https://gist.github.com/and-semakin/6080c25e106dedcecb0326aa4514b738.js?file=bad_code.py"></script>

Возможно, вам не видно всего, но в этом коде точно есть следующие "запахи кода":

* `import *` — импортирование всех имен из модуля, хотя используется
из них только одно;
* `import itertools` — ненужный импорт;
* во множестве мест стоят лишние или отсутствующие пробелы;
* название функции написано в стиле PascalCase;
* в некоторых местах используются табы для отступов;
* используется список (изменяемый объект) в качестве значения аргумента
функции по умолчанию;
* используется слишком “широкое” выражение `except:` без указания
конкретного исключения.

Давайте посмотрим, что `flake8` скажет по поводу этого файла:

```sh
$ flake8 bad_code.py
bad_code.py:1:1: F403 'from math import *' used; unable to detect undefined names
bad_code.py:2:1: F401 'itertools' imported but unused
bad_code.py:4:1: E302 expected 2 blank lines, found 1
bad_code.py:4:4: E271 multiple spaces after keyword
bad_code.py:4:25: E211 whitespace before '('
bad_code.py:4:33: E202 whitespace before ')'
bad_code.py:5:1: W191 indentation contains tabs
bad_code.py:5:8: E271 multiple spaces after keyword
bad_code.py:5:10: F405 'sqrt' may be undefined, or defined from star imports: math
bad_code.py:5:21: E202 whitespace before ')'
bad_code.py:7:1: E302 expected 2 blank lines, found 1
bad_code.py:7:23: E741 ambiguous variable name 'l'
bad_code.py:8:1: E101 indentation contains mixed spaces and tabs
bad_code.py:9:1: E101 indentation contains mixed spaces and tabs
bad_code.py:11:1: E305 expected 2 blank lines after class or function definition, found 1
bad_code.py:12:1: E101 indentation contains mixed spaces and tabs
bad_code.py:13:1: E101 indentation contains mixed spaces and tabs
bad_code.py:13:20: E225 missing whitespace around operator
bad_code.py:14:1: E101 indentation contains mixed spaces and tabs
bad_code.py:14:67: W291 trailing whitespace
bad_code.py:15:1: E101 indentation contains mixed spaces and tabs
bad_code.py:15:14: W291 trailing whitespace
bad_code.py:16:1: E101 indentation contains mixed spaces and tabs
bad_code.py:16:5: E722 do not use bare 'except'
bad_code.py:17:1: E101 indentation contains mixed spaces and tabs
```

Как видите, `flake8` нашёл кучу ошибок. Для каждой ошибки указана строка
и номер символа в строке (не всегда точный), где произошла ошибка.
Также у каждой категории ошибок есть свой код: `E101`, `W291` и т.д.
Эти коды ошибок могут использоваться для включения/отключения правил.
Тем не менее, не все ошибки были найдены. Давайте установим пару плагинов,
чтобы добавить ещё правил!

### Плагины

Как я уже говорил, для `flake8` написано множество плагинов.
Обычно плагины легко гуглятся или находятся в [списках плагинов](https://github.com/DmytroLitvinov/awesome-flake8-extensions).
Есть плагины для всех популярных фреймворков и библиотек — пользуйтесь ими!
Давайте для нашего простого примера установим
[`flake8-bugbear`](https://github.com/PyCQA/flake8-bugbear)
(находит распространённые логические ошибки) и 
[`pep8-naming`](https://github.com/PyCQA/pep8-naming)
(проверяет имена на соответствие PEP8).

Плагины устанавливаются так же, как и сам `flake8` (для краткости я
не буду писать примеры для `pipenv` и `poetry` — сами сможете обобщить):

```sh
$ pip install flake8-bugbear pep8-naming
```

Давайте убедимся, что плагины действительно установились
и `flake8` может их найти:

```sh
$ flake8 --version
3.8.1 (flake8-bugbear: 20.1.4, mccabe: 0.6.1, naming: 0.10.0, pycodestyle: 2.6.0, pyflakes: 2.2.0) CPython 3.8.2 on Linux
```

Если вы видите в списке в скобках названия ваших плагинов, то всё хорошо.

Теперь снова проверим наш файл:

```sh
$ flake8 bad_code.py
bad_code.py:1:1: F403 'from math import *' used; unable to detect undefined names
bad_code.py:2:1: F401 'itertools' imported but unused
bad_code.py:4:1: E302 expected 2 blank lines, found 1
bad_code.py:4:4: E271 multiple spaces after keyword
bad_code.py:4:6: N802 function name 'CalculateSquareRoot' should be lowercase
bad_code.py:4:25: E211 whitespace before '('
bad_code.py:4:28: N803 argument name 'Number' should be lowercase
bad_code.py:4:33: E202 whitespace before ')'
bad_code.py:5:1: W191 indentation contains tabs
bad_code.py:5:8: E271 multiple spaces after keyword
bad_code.py:5:10: F405 'sqrt' may be undefined, or defined from star imports: math
bad_code.py:5:21: E202 whitespace before ')'
bad_code.py:7:1: E302 expected 2 blank lines, found 1
bad_code.py:7:23: E741 ambiguous variable name 'l'
bad_code.py:7:25: B006 Do not use mutable data structures for argument defaults.  They are created during function definition time. All calls to the function reuse this one instance of that data structure, persisting changes between them.
bad_code.py:8:1: E101 indentation contains mixed spaces and tabs
bad_code.py:9:1: E101 indentation contains mixed spaces and tabs
bad_code.py:11:1: E305 expected 2 blank lines after class or function definition, found 1
bad_code.py:12:1: E101 indentation contains mixed spaces and tabs
bad_code.py:13:1: E101 indentation contains mixed spaces and tabs
bad_code.py:13:20: E225 missing whitespace around operator
bad_code.py:14:1: E101 indentation contains mixed spaces and tabs
bad_code.py:14:67: W291 trailing whitespace
bad_code.py:15:1: E101 indentation contains mixed spaces and tabs
bad_code.py:15:14: W291 trailing whitespace
bad_code.py:16:1: E101 indentation contains mixed spaces and tabs
bad_code.py:16:5: E722 do not use bare 'except'
bad_code.py:16:5: B001 Do not use bare `except:`, it also catches unexpected events like memory errors, interrupts, system exit, and so on.  Prefer `except Exception:`.  If you're sure what you're doing, be explicit and write `except BaseException:`.
bad_code.py:17:1: E101 indentation contains mixed spaces and tabs
```

В выводе появились новые категории ошибок (`N802`, `B006`)
— они как раз добавлены плагинами. На этот раз, как мне кажется,
найдены все ошибки. К сожалению, `flake8` не умеет сам чинить
найденные ошибки, поэтому давайте сделаем это вручную:

<script src="https://gist.github.com/and-semakin/6080c25e106dedcecb0326aa4514b738.js?file=not_so_bad_code.py"></script>

Обратите внимание на строки 8 и 10, там содержится комментарии `# noqa`.
При помощи этих комментариев можно заставить `flake8` игнорировать ошибки.
Это бывает полезно, когда по какой-то причине код должен остаться именно
таким, например:

* он автоматически сгенерирован и исправление в нём ошибок не имеет смысла;
* исправление этой ошибки породит куда более уродливый код,
чем комментарий `# noqa`;
* у вас просто сейчас нет времени, чтобы исправлять эту ошибку
(плохая отмазка, серьёзно).

Если не указать код ошибки, то будут проигнорированы все ошибки в строке
— я не рекомендую так делать, потому что так можно пропустить
и на самом деле плохие ошибки. Если указать номер правила, то
`flake8` будет игнорировать только указанную категорию,
а о других ошибках в этой же строке доложит.
Вообще, комментариями `# noqa` нужно пользоваться с большой осторожностью.
Считайте, что каждый раз, когда вы это делаете, вы берёте на
себя ответственность за эту строку кода. Если программа сломается
в этом месте, то пеняйте на себя — <s>минздрав</s> линтер вас предупреждал.


### Конфигурация

`flake8` для работы не требует никакой конфигурации.
Он имеет достаточно (но не слишком) строгие настройки по умолчанию,
которые подойдут большинству пользователей, но иногда бывает нужно
отключить (или наоборот включить) определённые правила на уровне всего проекта.
Сделать это можно через файлы `.flake8` или `setup.cfg` в корне проекта.
Если у вас в проекте уже есть файл `setup.cfg`, то можно добавить конфигурацию
`flake8` в него. Если вы предпочитаете для каждой утилиты держать
отдельный файл конфигурации, то используйте `.flake8`. В любом случае,
формат для обоих этих файлов совпадает:

```ini
[flake8]
ignore = D203,E741
exclude =
    # No need to traverse our git directory
    .git,
    # There's no value in checking cache directories
    __pycache__,
    # The conf file is mostly autogenerated, ignore it
    docs/source/conf.py,
    # The old directory contains Flake8 2.0
    old,
    # This contains our built documentation
    build,
    # This contains builds of flake8 that we don't want to check
    dist
max-complexity = 10
```

В конфигурации можно перечислить игнорируемые правила и директории,
в которые `flake8` заглядывать не будет, а также максимальную
[цикломатическую сложность](https://ru.wikipedia.org/wiki/%D0%A6%D0%B8%D0%BA%D0%BB%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D1%81%D0%BB%D0%BE%D0%B6%D0%BD%D0%BE%D1%81%D1%82%D1%8C)
для функций. Все эти настройки будут автоматически применяться
к запускам `flake8` во всех поддиректориях проекта.

Если же вам не хватает какого-нибудь правила, и его нет даже в уже
готовых плагинах, то [написание собственного плагина](https://flake8.pycqa.org/en/latest/plugin-development/)
— не такая уж и сложная задача.
[Я попробовал](https://github.com/and-semakin/flake8-pytestrail/),
у меня на это ушло 2-3 часа.

## pylint

`pylint` — это ещё один популярный линтер для Python.
Этот линтер значительно умнее и продвинутее `flake8`.
В `pylint` из коробки заложено очень много правил и рекомендаций,
и по умолчанию они все включены, так что он достаточно строгий и придирчивый.
Чтобы интегрировать его в существующий большой проект придётся потратить
некоторое время, чтобы выбрать те правила, которые для вас важны.
Так же как и `flake8`, `pylint` поддерживает плагины для расширения
базовой функциональности, но насколько я вижу, экосистема плагинов у `pylint`
значительно беднее.

Также при каждом запуске `pylint` выводит оценку качества кода
по десятибалльной шкале, а также следит, как эта оценка меняется
с течением времени. Достичь десятки очень сложно, но это благородная цель,
к которой нужно стремиться.

### Установка

Установка `pylint` принципиально ничем не отличается от установки `flake8`.
Выполнить внутри виртуального окружения проекта:

```sh
$ pip install pylint
```

Для `pipenv`:

```sh
$ pipenv install --dev pylint
```

Для `poetry`:

```sh
$ poetry add --dev pylint
```


### Использование

`pylint` можно натравить на определённый файл:

```sh
$ pylint file.py
```

С директориями у `pylint` дела обстоят чуть сложнее. Все директории он
обрабатывает как питоновские модули, поэтому если в директории нет хотя бы
пустого файла `__init__.py`, то работать с ней `pylint` не сможет. Имейте
это ввиду.

Давайте попросим `pylint` прокомментировать файл с плохими практиками
из предыдущего примера:

```sh
$ pylint bad_code.py
************* Module bad_code
bad_code.py:4:25: C0326: No space allowed before bracket
def  CalculateSquareRoot (Number ):
                         ^ (bad-whitespace)
bad_code.py:4:33: C0326: No space allowed before bracket
def  CalculateSquareRoot (Number ):
                                 ^ (bad-whitespace)
bad_code.py:5:0: W0312: Found indentation with tabs instead of spaces (mixed-indentation)
bad_code.py:5:21: C0326: No space allowed before bracket
	return  sqrt(Number )
                     ^ (bad-whitespace)
bad_code.py:13:19: C0326: Exactly one space required around assignment
        your_number=float(input('Enter your number: '))
                   ^ (bad-whitespace)
bad_code.py:14:66: C0303: Trailing whitespace (trailing-whitespace)
bad_code.py:15:13: C0303: Trailing whitespace (trailing-whitespace)
bad_code.py:1:0: W0622: Redefining built-in 'pow' (redefined-builtin)
bad_code.py:1:0: C0114: Missing module docstring (missing-module-docstring)
bad_code.py:1:0: W0401: Wildcard import math (wildcard-import)
bad_code.py:4:0: C0103: Function name "CalculateSquareRoot" doesn't conform to snake_case naming style (invalid-name)
bad_code.py:4:0: C0103: Argument name "Number" doesn't conform to snake_case naming style (invalid-name)
bad_code.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
bad_code.py:7:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
bad_code.py:7:0: C0103: Argument name "l" doesn't conform to snake_case naming style (invalid-name)
bad_code.py:7:0: C0116: Missing function or method docstring (missing-function-docstring)
bad_code.py:16:4: W0702: No exception type(s) specified (bare-except)
bad_code.py:1:0: W0614: Unused import acos from wildcard import (unused-wildcard-import)
bad_code.py:1:0: W0614: Unused import acosh from wildcard import (unused-wildcard-import)
bad_code.py:1:0: W0614: Unused import asin from wildcard import (unused-wildcard-import)
bad_code.py:1:0: W0614: Unused import asinh from wildcard import (unused-wildcard-import)
...
bad_code.py:2:0: W0611: Unused import itertools (unused-import)
-------------------------------------
Your code has been rated at -41.43/10
```

Я немного сократил вывод. Как видите, даже без плагинов `pylint` нашёл
все ожидаемые ошибки, и даже больше — например, он даже предлагает написать
документацию.

По каждой ошибке можно запросить более подробную справку, используя
название правила из конца строки с ошибкой или код:

```sh
$ pylint --help-msg=missing-docstring
$ pylint --help-msg=R0902
```

Вот какие ошибки `pylint` находит для файла, который с точки зрения `flake8`
не содержит никаких ошибок:

```sh
$ pylint not_so_bad_code.py 
************* Module not_so_bad_code
not_so_bad_code.py:1:0: C0114: Missing module docstring (missing-module-docstring)
not_so_bad_code.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
not_so_bad_code.py:8:0: C0103: Argument name "l" doesn't conform to snake_case naming style (invalid-name)
not_so_bad_code.py:8:0: C0116: Missing function or method docstring (missing-function-docstring)
not_so_bad_code.py:20:11: W0703: Catching too general exception Exception (broad-except)
-----------------------------------
Your code has been rated at 6.67/10
```

А вот так в `pylint` можно игнорировать отдельную ошибку на строке прямо в файлах
с кодом:

```python
def append_item(item, l=None):  # pylint: disable=C0103
   ...
```

Ещё `pylint` умеет игнорировать ошибки в блоках кода:

```python
def test():
    # Disable all the no-member violations in this function
    # pylint: disable=no-member
    ...
```

И для файлов целиком. Вот так можно отключить все ошибки из категорий
Warning, Convention и Refactor:

```python
# pylint: disable=W,C,R
```

А можно не проверять файл вообще:

```python
# pylint: skip-file
```

Подробнее о правилах управления сообщениями
[смотрите в документации](http://pylint.pycqa.org/en/latest/user_guide/message-control.html).
Для более сложной настройки правил, придётся по-настоящему сконфигурировать
`pylint`.

### Конфигурация

`pylint` настраивается через файл `.pylintrc` в корне проекта. Чтобы создать
дефолтный файл конфигурации, нужно выполнить следующую команду:

```sh
$ pylint --generate-rcfile > .pylintrc
```

Созданный файл содержит все поддерживаемые `pylint` опции с довольно
подробными комментариями, так что углубляться я не буду.

### Плагины

Давайте установим какой-нибудь популярный плагин, например,
[`pylint-django`](https://pypi.org/project/pylint-django/):

```sh
$ pip install pylint-django
```

Теперь запускать `pylint` нужно вот так:

```sh
$ pylint --load-plugins pylint_django [..other options..] <path_to_your_sources>
```

либо в `.pylintrc` нужно исправить директиву `load-plugins`:

```text
load-plugins=pylint_django
```

## Интеграция линтера в проект

Интегрировать линтер в проект можно на трёх уровнях.
Я рекомендую по возможности использовать все три, но обязательным
является как минимум один (лучше всего, чтобы это была CI система).

### Редактор кода или IDE

Популярные IDE для Python умеют легко интегрировать с линтерами и
подсвечивать ошибки линтера прямо в редактируемом файле.
Это удобно, потому что позволяет не выходя из редактора получить
полезную обратную связь.

PyCharm автоматически находить установленные `flake8` и `pylint` внутри
[интерпретатора проекта](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html)
и подключается к ним.

VS Code требует небольшой настройки, которая
[описана здесь](https://code.visualstudio.com/docs/python/linting).


### Git-хуки

> Также читайте [пост про Git-хуки и `pre-commit`]({filename}pre-commit.md).

В git есть [возможность запрограммировать](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
определенные скрипты (хуки) в ответ на действия пользователя.
Например, можно запускать
какие-нибудь проверки перед коммитом, заново скачивать зависимости проекта
при переключении веток, высылать сообщение в рабочий чат
после пуша в удалённый репозиторий и вообще что угодно.

![я запушель]({static}/static/i_have_pushed_meme.jpg)

Нас интересует возможность запускать линтер перед коммитом так,
чтобы если линтер найдёт какие-нибудь проблемы, операция коммита прерывалась.
Git-хуки можно настроить, написав несложный shell-скрипт,
но я рекомендую использовать для этого специальные утилиты,
такие как [pre-commit](https://pre-commit.com/).
[Вот здесь](https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/)
можно найти описание процесса настройки запуска `flake8` через `pre-commit`.

Обратите внимание, что Git-хуки нужно будет настроить на машине каждого
разработчика в проекте.

### Continuous Integration (CI)

Последний эшелоном защиты от попадания “сломанного” кода в основную ветку
репозитория является система непрерывной интеграции (CI) — такая, как:

* [GitHub Actions](https://help.github.com/en/actions);
* [GitLab CI](https://docs.gitlab.com/ce/ci/)
(а ещё читайте пост в блоге моего хорошего товарища про
[основы GitLab CI](https://alse-code.ru/gitlab-ci-intro/));
* [Travis CI](https://travis-ci.org/);
* или [другая](https://github.com/ligurio/awesome-ci).

На каждый пуш в репозиторий система непрерывной интеграции должна
запускать проверки (включая все линтеры и тесты), и если что-то идёт
не так, рядом с коммитом должен появиться красный крестик.
Ветку с таким коммитом на конце нельзя будет слить с основной
веткой проекта через пулл-реквест на GitHub (или мёрдж-реквест на GitLab).
[Пример того, как настроить GitHub Actions](https://help.github.com/en/actions/language-and-framework-guides/using-python-with-github-actions#starting-with-the-python-workflow-template)
для запуска `flake8` и других питоновских проверок.

CI — это единственный надёжный способ обеспечить качество кода.
Предыдущие способы нужны скорее для удобства разработчика, чтобы он
как можно скорее получал обратную связь, но разработчик вправе проигнорировать
или отключить эти предупреждения.

# Заключение

В подзаголовке этой статьи я написал фразу, что линтер способен
сэкономить разработчику один день жизни в месяц. Фраза может показаться
кликбейтной, но, поверьте мне, это так это и работает.
Возможно, я даже преуменьшил.
Чем раньше найдена ошибка, тем быстрее идёт разработка.
Иногда линтер предотвращает баги, иногда спасает от мучительного
траблшутинга. Линтеры абсолютно точно значительно сокращают время,
потраченное коллегами на код-ревью, потому что все тривиальные
ошибки будут отловлены автоматикой.

Не стоит недооценивать линтеры. Это те инструменты,
которые делают из “кодера” настоящего “software engineer”,
из мальчика — мужчину. Если вы до сих пор не пользуетесь каким-нибудь
линтером, то рекомендую всерьез задуматься над внедрением!

Я предпочитаю использовать `flake8`, потому что он простой
и понятный, как топор. С ним легко работать, его легко настроить
под свои нужды, а почти любые недостающие правила можно получить
через уже готовые плагины.

У `pylint` тоже есть свои последователи. Его ценят за подробный вывод
и большое количество правил в стандартной поставке.
Мне же `pylint` всегда казался слишком сложным в эксплуатации.

А кто-то вообще рекомендует устанавливать `flake8` и `pylint` параллельно.

Если понравилась статья, то
[подпишитесь на уведомления]({filename}../pages/subscribe.md)
о новых постах в блоге, чтобы ничего не пропустить!

# Дополнительное чтение

* [документация `flake8`](https://flake8.pycqa.org/en/latest/);
* [исходный код `flake8`](https://gitlab.com/pycqa/flake8);
* [список плагинов `flake8`](https://github.com/DmytroLitvinov/awesome-flake8-extensions);
* [сайт, где можно посмотреть правила `flake8`](https://lintlyci.github.io/Flake8Rules/);
* [документация `pylint`](http://pylint.pycqa.org/en/latest/);
* [исходный код `pylint`](https://github.com/PyCQA/pylint);
* [обсуждение “flake8 vs pylint” на Reddit](https://www.reddit.com/r/Python/comments/82hgzm/any_advantages_of_flake8_over_pylint/);
* [пост на RealPython про качество кода](https://realpython.com/python-code-quality/);
* [статья на Хабре про линтеры](https://habr.com/ru/company/dataart/blog/318776/).

*Обложка: [Sa Mu, Traffic Light](https://flic.kr/p/DQTiBS)*
