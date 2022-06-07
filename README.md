
# File server project

Author is Maxim Suslov.

## Список заданий

В тренинге имеется набор заданий, которые нужно выполнить последовательно, чтобы получить итоговый проект.

Информация по каждому заданию находится в отдельной ветке:

| Задание                 | Ветка             |
| ----------------------- | ----------------- |
| 01. Настройка окружения | `01_prepare_env`  |
| 02. Файловый сервис     | `02_file_service` |
| 03. Логирование         | `03_logging`      |
| 04. Настройка программы | `04_config`       |
| 05. REST API            | `05_rest_api`     |
| 06. Web                 | `06_web`          |
| 07. Database            | `07_database`     |

Решение для каждого задания представлено в ветке с таким же названием, но с суффиксом `_solution`.

> Например, решение для задания "01. Настройка окружения" находится в ветке `01_prepare_env_solution`.

Студент может обратиться к этой ветке, чтобы свериться с возможным решением или взять за основу при работе со следующим заданием.

## Начало нового задания, продолжая текущий проект

Каждое задание должно выполняться в отдельной ветке. См. [Список заданий].

> Например, первое задание должно выполняться в ветке `01_prepare_env`.

Для того чтобы начать новое здание, вам необходимо сделать ветку с таким названием на верхушке ветки `master`:

```console
$ git checkout -b BRANCH_NAME master
```

Далее необходимо подгрузить задание с одноимённой ветки с сервера:

```console
$ git cherry-pick trainer/BRANCH_NAME
```

Проверьте наличие конфликтов в выводе команды `git status`. Если они есть, то разрешите их.

Пример команд для старта первого задания:

```console
$ git checkout -b 01_prepare_env master
$ git fetch trainer
$ git cherry-pick trainer/01_prepare_env
$ git status
# исправление конфликтов, если есть и далее
$ git commit
```

Теперь в папке `tasks` появится файл с очередным заданием.

## Начало нового задания с нуля

Иногда студент пропускает часть материала и хочет начать с определённого задания. В этом случае нужно взять решение предыдущего задания:

```console
$ git checkout -b BRANCH_NAME PREV_BRANCH_NAME_solution
```

См. [Список заданий] для перечня заданий и веток, где они находятся.

## Отправка изменений на ревью

После выполнения задания студент должен создать коммит:

```console
$ git status
$ git diff
$ git add file1 file2 ...
$ git commit
```

и отправить изменения на сервер:

```console
$ git push -u origin BRANCH_NAME  # в первый раз
$ git push                        # в последующие разы
```

Затем сделать pull/merge-request из текущей ветки в ветку `master` и пригласить преподавателя.

Если во время ревью были найдены ошибки, то студент исправляет их и создаёт новый коммит. А затем снова отправляет изменения на сервер и уведомляет преподователя.

Когда ошибок нет или они все исправлены, преподователь ставить approve и изменения интегрируются в ветку `master` на сервере. Теперь эти изменения нужно скопировать к себе на локальный репозиторий:

```console
$ git checkout master
$ git pull
```

## Получение изменений с сервера

Иногда по ходу тренинга задания могут обновляться.

Для получения изменения с репозитория тренера выполните следующие команды:

```console
$ git fetch trainer
```

Далее, если у вас уже была создана локальная ветка и вы начали работу над заданием, то влейте новые изменения к себе:

```console
$ git merge trainer/BRANCH_NAME
```


[Список заданий]: #список-заданий

# Requirements

## General

- [x] Support Python 3.7+
- [x] Use venv during the development
- [ ] Program must work both on Linux and Windows
- [x] Specify directory to keep manage files via CLI arguments
- [x] Cover functionality using `pytest`
- [ ] Deploy via Docker image (for those who is familiar with Docker)
- [x] Use `logging` module for logging

## File Service

- [x] Avoid usage of dangerous values like `../../../etc/passwd`
- [ ] Support binary file content as well

## Configuration

- [x] Read settings from CLI arguments
- [x] Read settings from env vars
- [x] Read settings from config file

## Web Service

- [ ] Specify web-server port via CLI arguments
- [ ] Work independently without WSGI
- [ ] Suit with RESTful API requirements
- [ ] Use asynchronous programming concept (aiohttp?)
- [ ] Use multithreading for downloading files
- [ ] Partial file download (http range)

## Crypto Service

- [ ] Protect files by cryptography tools

## Auth Service

- [ ] Provide access to files via access policy
- [ ] Keep users in database
