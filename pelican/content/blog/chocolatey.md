Title: Chocolatey — пакетный менеджер для Windows
Tags: windows, choco
Summary: Самая важная программа для любителей окошек.
Header_cover: /static/chocolate.jpg
Status: published

Как сказал один мудрец (и по совместительству просто мой друг):

> “нет плохих или хороших операционных систем, есть подходящие и
> не подходящие для решения конкретных пользовательских задач”.

Глубокая мысль, я с этим полностью согласен.
Хотя для решения конкретно моих рабочих задач намного лучше подходят
другие ОС, у Windows тоже есть своя ниша.
Я уже давно привык пользоваться в повседневной деятельности
Unix-подобными операционными системами, такими как Fedora Linux и macOS.
Но недавно я решил совершить очередной набег в мир Windows
— попробовать новые классные фичи [WSL2](https://docs.microsoft.com/ru-ru/windows/wsl/)
да в игры поиграть.

Только в этот раз я решил сразу сделать всё по-правильному, и
устанавливать весь софт так, чтобы им потом было удобно управлять и обновлять.
В поисках решения этой задачи я открыл для себя
[замечательный инструмент Chocolatey](https://chocolatey.org/),
который теперь считаю жизненно необходимым для комфортного пользования
Windows.

Chocolatey — это пакетный менеджер для Windows,
примерно как [`apt`](https://ru.wikipedia.org/wiki/Advanced_Packaging_Tool)
в мире Debian/Ubuntu или
[`dnf`](https://ru.wikipedia.org/wiki/DNF_(%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80_%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2))
в мире Fedora/CentOS.
Пакетный менеджер занимается установкой, удалением и обновлением программ.
Если вам, как и мне, надоело ставить галочки под текстом лицензии
(хоть раз вообще читали?)
и безразлично нажимать кнопку “далее”, то Chocolatey вам поможет.
Он имеет интерфейс командной строки — то, что надо для такого гика, как я!
У Chocolatey [большая библиотека пакетов](https://chocolatey.org/packages)
— больше 7500 штук, всё популярное там точно есть.

Хоть я привёл в пример `apt` и `dnf`, на самом деле,
Chocolatey имеет намного больше общего с
[Homebrew — пакетным менеджером для macOS](https://ru.wikipedia.org/wiki/Homebrew_(%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80_%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2_%D0%B2_Mac_OS)).
В Linux пакетные менеджеры уже давно стали насущной необходимостью
— там этим никого не удивить, а Chocolatey и Homebrew работают в окружениях,
где изначально пакетные менеджеры не предусмотрены.
При этом оба они отлично справляются со своими задачами.

Chocolatey написан на C# и PowerShell, имеет
[открытый исходный код](https://github.com/chocolatey/choco).
Для работы требует Windows 7 или новее.

## Установка

Чтобы установить Chocolatey, нужно запустить командную строку
с правами администратора. Сделать это в Windows 10 можно так:

1. Нажимаем на клавиатуре кнопку Win или просто открываем меню "Пуск";
2. Набираем `cmd`;
3. На найденной программе нажимаем правой кнопкой мыши
и выбираем пункт “Run as administrator” или, в русской локализации,
“Запуск от имени администратора”.

![Run as administrator]({static}/static/cmd_run_as_administrator.jpg)

В открывшееся окно терминала нужно вставить следующую команду:

```sh
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command " [System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
```

На всякий случай, если эта команда устареет и перестанет работать,
или вы предпочитаете вставлять в администраторский терминал команды
только из официальных источников (и правильно делаете), то документация
по установке находится
[вот здесь](https://chocolatey.org/docs/installation#install-with-cmdexe).

После того, как команда отработает (у меня установка заняла примерно минуту),
нужно перезапустить терминал. Вместо `cmd`
можно запустить PowerShell (тоже от имени администратора) — он немного
удобнее. Можно проверить установку:

```sh
choco -?
```

Если вы видите справку по команде, то установка прошла успешно.


## Установка программ

Давайте установим через `choco` первые программы.
Все эти программы найдены в [реестре пакетов](https://chocolatey.org/packages)
и проверены мной — работают.
При установке вы можете заметить, что все программы скачиваются с
официальных сайтов разработчиков.
Если вы переживаете по поводу вирусов, то рекомендую почитать,
[какие меры предпринимают мейнтейнеры Chocolatey](https://chocolatey.org/docs/security),
чтобы обеспечить безопасность пакетов (там всё серьезно).

Во всех командах я добавил флаг `-y`, чтобы установщик не задавал
вообще никаких вопросов. Эта команда автоматически соглашается с
лицензиями и разрешает запуск скриптов установки. Ради интереса
можете попробовать убрать этот флаг из команд, и посмотреть, что будет.

Допустим, что вам нужен браузер (удалите из команды ненужные названия):

```sh
choco install -y googlechrome firefox
```

Или текстовый редактор/IDE (удалите из команды ненужные названия):

```sh
choco install -y notepadplusplus.install vscode
```

Я являюсь заядлым пользователем PyCharm, который лучше всего устанавливать
через [JetBrains Toolbox](https://www.jetbrains.com/ru-ru/toolbox-app/)
(как и любые другие IDE от JetBrains):

```sh
choco install -y jetbrainstoolbox
```

Инструменты для разработки:

```sh
choco install -y git python3 microsoft-windows-terminal postman
```

Мессенджеры и видео-конференции:

```sh
choco install -y telegram.install slack zoom 
```

Игры:

```sh
choco install -y steam epicgameslauncher
```

Всякое прочее-разное полезное:

```sh
choco install -y 7zip vlc paint.net teamviewer qbittorrent thunderbird putty.install
```

И для установки даже не пришлось кликать мышью по кнопкам!

[Тут](https://chocolatey.org/docs/commands-uninstall) можете почитать
про удаление программ при помощи `choco`.


## Обновление

Вот так можно обновить все установленные через `choco` программы
до актуальных версий:

```sh
choco upgrade all -y
```

По-моему, это очень круто и удобно!


# Заключение

`choco` — теперь для меня это просто маст-хэв на Windows.
Самая первая программа, которую я буду устанавливать.
Благодаря Chocolatey, для меня Windows стала немного дружелюбнее.
Всем рекомендую попробовать!

Если понравилась статья, то
[подпишитесь на уведомления]({filename}../pages/subscribe.md)
о новых постах в блоге, чтобы ничего не пропустить!

# Дополнительное чтение

* [официальный сайт Chocolatey](https://chocolatey.org/);
* [реестр пакетов](https://chocolatey.org/packages);
* [исходный код](https://github.com/chocolatey/choco);
* [видео про Chocolatey для тех, кто больше любит воспринимать информацию визуально](https://www.youtube.com/watch?v=hfgZYpo5moA).

*Обложка: [Jean Beaufort, Chocolate](https://www.publicdomainpictures.net/ru/view-image.php?image=285902&picture=)*
