# Commit: guard ask endpoint for missing index_path

## Цель шага

Сделать поведение `/ask` честным и предсказуемым, если клиент передаёт путь к несуществующему локальному индексу.

## Почему этот шаг был выделен отдельно

В рабочем дереве уже смешаны несколько разных API- и frontend-изменений: CORS для локального demo, дополнительные проверки `/index`, изменения README и незакоммиченный frontend. Проверка `index_path` для `/ask` — отдельный маленький failure mode, который можно безопасно выделить и зафиксировать без смешивания с остальными шагами.

## Какое состояние репозитория было до этого

В `backend/app/api.py` endpoint `/ask` сразу вызывал `_ask_grounded_question(...)` и не проверял, существует ли `index_path` на диске. При ошибочном пути поведение зависело от более глубокого слоя загрузки индекса и не оформлялось как явная API-ошибка на границе HTTP.

## Что изменено

- В `backend/app/api.py` добавлена ранняя проверка существования `index_path`.
- Для отсутствующего файла API теперь возвращает `HTTP 404` с детерминированным `detail`.
- В `backend/tests/test_api.py` добавлен узкий regression test на запрос `/ask` с несуществующим `index_path`.

## Как работает итоговое решение

Перед вызовом `_ask_grounded_question(...)` endpoint `/ask` делает `Path(request.index_path).exists()`. Если файл отсутствует, API сразу отвечает `404` и возвращает сообщение вида `index_path does not exist: ...`. До retrieval и answer layer такой запрос больше не доходит.

## Почему эти изменения нельзя было смешивать с другими

Этот шаг касается только одного входного контракта `/ask`. Смешивание его с CORS, frontend demo, валидациями `/index` или документационным пакетом для агентов сделало бы историю менее читаемой и ухудшило бы привязку "один failure mode — один commit".

## Какие файлы изменены

- `backend/app/api.py`
- `backend/tests/test_api.py`
- `docs/commit-notes/README.md`
- `docs/commit-notes/2026-04-14-api-ask-missing-index-404.md`

## Какие проверки запущены

- `python3 -m unittest backend.tests.test_api.ApiTests.test_ask_endpoint_returns_404_for_missing_index`
- `python3 -m py_compile backend/app/api.py backend/tests/test_api.py`

## Результат проверки

- `python3 -m unittest ...` не выполнился в текущем окружении, потому что локальный Python не содержит установленный пакет `fastapi` (`ModuleNotFoundError` при импорте `fastapi.testclient`).
- `python3 -m py_compile backend/app/api.py backend/tests/test_api.py` прошёл успешно.

## Что осталось вне этого коммита

- незакоммиченный frontend-каркас и frontend demo;
- CORS-настройка FastAPI для локального frontend;
- проверки `/index` на missing directory и file path;
- дополнительные README/architecture/evaluation changes;
- agent-support документы (`SONNET.md`, playbook, workflow, project map, review template).

## Следующий логичный маленький шаг

Следующим продуктовым шагом остаётся backend-only Docker image из `docs/NEXT_STEP.md`: `Dockerfile.backend` и точные команды проверки `/health` в контейнере.
