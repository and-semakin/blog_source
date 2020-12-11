# Исходники блога

Сгенерировано на основе вот этого cookie-cutter шаблона: https://github.com/lgiordani/cookiecutter-pelicanblog

## Как этим пользоваться

1. Клонируешь репо (на машине должен быть настроен доступ к GitHub по SSH):

```sh
git clone git@github.com:and-semakin/blog_source.git
```

2. Запускаешь скрипт, который инициализирует окружение:

```sh
cd blog_source
./setup.sh
```

3. Устанавливаешь зависимости через `poetry`:

```sh
poetry install
```

Настраиваешь свой редактор на использование созданного виртуального окружения.
Путь к виртуальному окружению получается вот так:

```sh
poetry env info -p
```

4. Пишешь новый пост, коммитишь его исходники в этом репо:

```sh
git add pelican/content
git commit -m "Add new awesome post"
```

5. Генерируешь блог на основе новых исходников (внутри активированного виртуального окружения проекта):

```sh
./deploy.sh
```

6. Публикуешь блог через GitHub Pages:

```sh
./publish.sh
```

7. Проверяешь, что [блог](https://semakin.dev/) обновился.
