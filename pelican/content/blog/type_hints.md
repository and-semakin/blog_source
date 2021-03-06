Title: Аннотации типов в Python
Tags: python, typing, mypy
Summary: Введение в тайп-аннотации и тайп-чекинг в Python.
Header_cover: /static/lego_bits.jpg
Status: published


# Аннотации типов в Python

Python — это язык с сильной динамической типизацией.

* [Сильная](https://ru.wikipedia.org/wiki/%D0%A1%D0%B8%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F_%D0%B8_%D1%81%D0%BB%D0%B0%D0%B1%D0%B0%D1%8F_%D1%82%D0%B8%D0%BF%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F)
    — значит, что язык не допускает неявных приведений типов в неоднозначных
    ситуациях или когда будет утрачена точность, например, нельзя “сложить”
    число и строку.
* [Динамическая](https://ru.wikipedia.org/wiki/%D0%94%D0%B8%D0%BD%D0%B0%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D1%82%D0%B8%D0%BF%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F)
    — значит, что тип переменной определяется во время присваивания ей значения и
    может изменяться по ходу программы.

Такая система типов — это очень удачный компромисс между простотой разработки
и надежностью написанных программ, но она не лишена недостатков.

Например, объявления переменных с типами в языках со статической типизацией,
кроме своего основного назначения — инструкций компилятору или интерпретатору,
ещё и помогают программисту лучше понимать написанный код, служат своеобразной
документацией. Динамическая типизация не в состоянии этого дать.

Раньше, когда на Python писали в основном небольшие скрипты, это не было
такой уж острой проблемой, потому что всю программу за разумный промежуток
времени можно было охватить взглядом и понять. В последнее время язык стал
значительно популярнее.

> По данным исследований StackOverflow за
> [2020](https://insights.stackoverflow.com/survey/2020#most-popular-technologies),
> [2019](https://insights.stackoverflow.com/survey/2019#most-popular-technologies),
> [2018](https://insights.stackoverflow.com/survey/2018#most-popular-technologies),
> [2017](https://insights.stackoverflow.com/survey/2017#most-popular-technologies),
> [2016](https://insights.stackoverflow.com/survey/2016#technology-most-popular-technologies),
> [2015](https://insights.stackoverflow.com/survey/2015#tech-lang)
> (там же можно посмотреть результаты за 2014 и 2013)
> годы, Python с каждым годом
> растёт в популярности.

Сегодня на Python написано много сложных систем из сотен файлов и сотен тысяч
строк кода. В таких обстоятельствах документирующее свойство системы типов
становится очень полезным. В достаточно крупной кодовой базе при отсутствии
информации о типах очень сложно угадать
(а только гадать и остаётся), какие же именно объекты циркулируют по программе.

Кроме того, даже если код без информации о типах может быть и вполне
понятен человеку, например, благодаря удачно выбранным именам, то для
автоматики — это в любом случае абсолютно непроницаемый <s>черный</s>
непрозрачный ящик.
В такой ситуации очень сложно, не выполняя код (мы же говорим про статический
анализ), понять как он будет вести себя в ран-тайме. Аннотации типов позволяют
IDE, [линтерам]({filename}python_linters.md) и тайп-чекерам лучше понимать
код программы, что дает возможность
рано отлавливать достаточно хитрые ошибки. В конечном итоге это делает
написанные программы надежнее.

По этим соображениям, в Python 3.5 появился специальный синтаксис для
объявления типов параметров функций и их возвращаемых значений
([PEP 484](https://www.python.org/dev/peps/pep-0484/)).
В Python 3.6 эта возможность была расширена — стало можно объявлять типы
переменных вообще в любом месте программы
([PEP 526](https://www.python.org/dev/peps/pep-0526/)). С каждой новой версией
языка эта функциональность улучшается, и писать аннотации типов становится
всё проще, удобнее и естественнее, а экосистема вокруг типизированного
Python развивается семимильными шагами.

Нужно отметить, что тайп-аннотации — это именно возможность, а не обязанность.
У программиста есть выбор — добавлять информацию о типах или нет.
Таким образом Python пытается усидеть на двух стульях — остаться языком с
динамической типизацией и дать возможность для статического анализа написанных
программ. Привнести в хаос немного порядка, так сказать. И, по-моему, у Python 
это неплохо получается.

# Как это работает?

Программист при написании кода расставляет информацию о типах переменных,
параметров и возвращаемых значений функций. Это никак не влияет на выполнение 
программы. Python сам по себе никак не использует эту информацию в ран-тайме,
он лишь перекладывает её в специальные атрибуты функций или переменных,
делая доступной для сторонних утилит. То есть, если указано, что функция
принимает строки, то это никак не помешает вызвать её с целыми числами или
списками — в зависимости от тела функции, она может отработать, а может
завершиться ошибкой, но сама возможность вызова с любыми типами аргументов
никак не ограничивается. 

Зачем же тогда писать тайп-аннотации?

* документация для разработчиков;
* сторонние утилиты и библиотеки могут использовать эту информацию по своему
усмотрению, например, выполняя проверки типов или приводя данные к нужному типу.

Первый пункт достаточно очевидный, а про второй мы поговорим чуть позже в
разделе про тайп-чекеры.

# Простые типы

Вот так, например, можно тайп-аннотировать простую функцию:

```python
def greeting(name: str = "world") -> str:
    return "Hello, " + name
```

Типы параметров, принимаемых функцией, записываются после имени параметра
через знак двоеточия, но перед значением по умолчанию, если оно присутствует.
Возвращаемое значение функции записывается после знака “стрелки”.

Теперь читатель просто взглянув на сигнатуру функции может понять, что функция
принимает строку и возвращает строку. Наверное, если передать в неё другой тип,
то она не сможет корректно отработать.

Точно так же можно использовать для тайп-аннотаций и любые другие базовые
(примитивные, не-контейнерные) типы в Python:
`int`, `float`, `bool`, `str`, `bytes`, `None` и вообще практически что угодно.
Чуть позже посмотрим, как типизировать контейнерные типы данных, такие как списки,
кортежи, словари и множества.

Вот так можно зааннотировать функцию, которая принимает два числа с плавающей
точкой и возвращает число с плавающей точкой:

```python
def body_mass_index(weight: float, height: float) -> float:
    return weight / height ** 2
```

А вот так функцию, которая принимает строку и булевый аргумент, но ничего не
возвращает:

```python
def print_hello(name: str, upper: bool = False) -> None:
    if upper:
        name = name.upper()
    print("Hello,", name)
```

Вот так можно аннотировать любые переменные в любом месте кода (Python 3.6+):

```python
name: str = "Andrey"
age: int = 25
is_sick_with_covid19: bool = False  # надеюсь
pi: float = 3.1415

# можно даже аннотировать переменные, не назначая им значения
foo: str
```

Если мы создадим свой класс, то его тоже можно использовать для аннотаций:

```python
class Example:
    pass

# довольно бессмысленно, но для примера пойдет
example_instance: Example = Example()
```


# Контейнерные типы и дженерики

Перейдем к более сложным типам, таким как списки, кортежи, словари и множества.
Можно аннотировать в лоб, используя сами имена классов:

```python
primes: list
person_info: tuple
stock_prices: dict
valid_answers: set
```

Это не слишком информативно, потому что кроме самого типа контейнера было бы
ещё полезно знать, какие данные он в себе содержит. Что такое `person_info`?
Кортеж чего?

В Python до версии 3.9 для этого придётся использовать отдельные классы из
модуля `typing`, потому что стандартные классы не представляют такой
функциональности. Делается это при помощи квадратных скобок, как будто мы
извлекаем что-то по индексу:

```python
from typing import List, Tuple, Dict, Set

# тип всех элементов списка
primes: List[int]

# тип каждого элемента кортежа
person_info: Tuple[str, int, float, float]

# тип ключей, тип значений
stock_prices: Dict[str, float]

# тип всех элементов множества
valid_answers: Set[str]
```

Начиная с Python 3.9 можно использовать стандартные классы в точно таких же
целях, ничего ниоткуда не импортируя:

```python
# будет работать только начиная с Python 3.9!

# тип всех элементов списка
primes: list[int]

# тип каждого элемента кортежа
person_info: tuple[str, int, float, float]

# тип ключей, тип значений
stock_prices: dict[str, float]

# тип всех элементов множества
valid_answers: set[str]
```

Согласитесь, так намного понятнее. Сразу видно, какой тип данных лежит
внутри контейнера. Такие типы называются обобщёнными (generic types).

Кстати, в типизации можно яснее увидеть разницу между тем как должны
использоваться списки и кортежи (`list` vs. `tuple`).

* Списки содержат однородные данные — они все должны быть одного типа,
иначе с таким списком будет тяжеловато работать.
* Кортеж, напротив, может содержать разнородные данные, которые в зависимости
от позиции могут иметь тот или иной тип.
* Список нужно использовать,
когда длина заранее неизвестна либо она переменна, например,
список пользователей.
* Кортеж нужно использовать, когда длина данных известна
заранее и строго фиксирована, например, как в записи из таблицы в СУБД.

Получается, кортеж — это не просто неизменяемый брат-близнец списка.

Если сильно хочется использовать кортеж как просто неизменяемую
последовательность однородных данных, то можно зааннотировать его вот так,
используя `...` (это специальный объект `Ellipsis`, записывается как многоточие,
при чтении исходников вслух в этом месте нужно делать драматическую паузу):

```python
# кортеж из строк, длина неизвестна
months: Tuple[str, ...]
```


# Составные типы

Часто случаются ситуации, когда нужно объединить несколько типов, например,
для того, чтобы указать, что функция может принимать и строки, и числа.
Этого можно достичь при помощи дженерик-типа `Union` из модуля `typing`:

```python
from typing import Union

def add_or_concatenate(a: Union[str, int], b: Union[str, int]):
    return a + b
```

Также очень часто возникает ситуация, когда возможно либо значение определенного
типа, либо `None`. Это настолько частая ситуация, что для этого даже сделали
отдельный дженерик-тип `Optional`:

```python

from typing import Optional, Union

# по сути это одно и то же, но первый вариант проще читается
phone: Optional[str]
phone: Union[str, None]
```

Также может возникнуть ситуация, когда не получается указать какой-либо
конкретный тип, потому что, например, функция может принимать на вход абсолютно
что угодно. Для этих случаев тоже есть специальный объект `typing.Any`:

```python
from typing import Any

def func(arg: Any) -> Any:
    return arg
```

Можно считать, что `Any` неявно подставляется везде, где не указан более
конкретный тип. Очень соблазнительно везде вставлять этот тип, но
настоятельно рекомендую использовать его только в крайних случаях, потому что
чрезмерное его использование сводит пользу от типизации на нет.

Вообще советую заглянуть в
[документацию модуля `typing`](https://docs.python.org/3/library/typing.html),
там есть много интересных классов на все случаи жизни.


# Проверка типов

Допустим, что тайп-аннотации написаны. Как начать получать от этого пользу?

В экосистеме Python есть несколько конкурирующих между собой тайп-чекеров,
например, [`mypy`](http://mypy-lang.org/),
[`pyre`](https://pyre-check.org/),
[`pytype`](https://github.com/google/pytype),
[`pyright`](https://github.com/Microsoft/pyright).
Самым популярным среди них является `mypy`, наверное, потому что одним из
ключевых его разработчиков является сам
[Гвидо ван Россум](https://ru.wikipedia.org/wiki/%D0%92%D0%B0%D0%BD_%D0%A0%D0%BE%D1%81%D1%81%D1%83%D0%BC,_%D0%93%D0%B2%D0%B8%D0%B4%D0%BE).
Давайте на `mypy` и остановимся.

Установим `mypy` в проект. Внутри виртуального окружения проекта нужно выполнить:

```sh
$ pip install mypy
```

Для `pipenv` и `poetry` соответственно вот так:

```sh
$ pipenv install --dev mypy
$ poetry add --dev mypy
```

Давайте напишем самый тривиальный пример программы с ошибкой:

```python
print("qwerty" + 1)
```

При выполнении, очевидно, программа завершится ошибкой:

```sh
$ python example.py
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    print("qwerty" + 1)
TypeError: can only concatenate str (not "int") to str
```

Давайте посмотрим, сможет ли тайп-чекер обнаружить эту проблему:

```sh
$ mypy example.py
example.py:1: error: Unsupported operand types for + ("str" and "int")
Found 1 error in 1 file (checked 1 source file)
```

Отлично! Не исполняя программу, `mypy` смог понять, что в ней присутствует ошибка.
Давайте запрячем эту же самую ошибку чуть глубже, используя функцию:

```python
def greet(name: str) -> None:
    print("Hello, " + name)

# правильный вызов
greet("world!")
# а вот тут будет ошибка
greet(5)
```

Проверим типы в этой программе:

```sh
$ mypy example2.py
example2.py:9: error: Argument 1 to "greet" has incompatible type "int"; expected "str"
Found 1 error in 1 file (checked 1 source file)
```

Тайп-чекер пропустил правильный вызов функции, но обнаружил вызов функции
с ошибкой.


# Заключение

Тайп-аннотации — это настолько круто и удобно, что, честно говоря, я уже плохо
представляю, как раньше (до Python 3.5) без этого люди вообще программировали.
Для меня это самый веский аргумент в пользу Python 3 и против Python 2.
Это незаменимый инструмент при разработке насколько-нибудь крупной программы.

Обязательно нужно интегрировать тайп-чекинг в свой редактор/IDE, чтобы ошибки
подсвечивались ещё на этапе написания кода. Можно интегрировать тайп-чекинг в
Git-хуки и CI.

На странице ["Awesome Python Typing"](https://github.com/typeddjango/awesome-python-typing)
можно найти ещё много полезных инструментов, которые пользуются тайп-аннотациями.

Если понравилась статья, то
[подпишитесь на уведомления]({filename}../pages/subscribe.md)
о новых постах в блоге, чтобы ничего не пропустить!

# Дополнительное чтение:

* введение в аннотации типов [часть 1](https://habr.com/ru/company/lamoda/blog/432656/) и [часть 2](https://habr.com/ru/company/lamoda/blog/435988/) на Хабре;
* [документация к модулю `typing`](https://docs.python.org/3/library/typing.html);
* [документация `mypy`](https://mypy.readthedocs.io/en/stable/);
* [репозиторий `mypy` на GitHub](https://github.com/python/mypy);
* [сайт `mypy`](http://mypy-lang.org/);
* [сайт `pyre`](https://pyre-check.org/);
* [репозиторий `pytype` на GitHub](https://github.com/google/pytype);
* [репозиторий `pyright` на GitHub](https://github.com/Microsoft/pyright);
* [Awesome Python Typing](https://github.com/typeddjango/awesome-python-typing);
* [ликбез по типизации в языках программирования](https://habr.com/ru/post/161205/) на Хабре.

*Обложка: [Windell Oskay, Technic Bits](https://flic.kr/p/4hABNH)*
