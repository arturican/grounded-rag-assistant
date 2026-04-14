# Commit: add regression coverage for missing index input_dir

## Цель шага

Довести до конца поведение `/index` для отсутствующей директории: закрепить его отдельным API regression test и human-readable note.

## Почему этот шаг выделен отдельно

Проверка на missing `input_dir` — самостоятельный failure mode. Её нельзя смешивать с CORS, frontend docs sync или file-vs-directory валидацией, потому что у каждого из этих сценариев свой контракт и своя причина сбоя.

## Какое состояние репозитория было до этого

К моменту этого коммита ранняя `404`-проверка для missing `input_dir` уже присутствовала в `backend/app/api.py`, но в рабочем дереве ещё не было отдельного зафиксированного regression test и отдельной note, закрывающих именно этот шаг.

## Что изменено

- В `backend/tests/test_api.py` добавлен узкий тест `test_index_endpoint_returns_404_for_missing_input_dir`.
- Добавлена note `docs/commit-notes/2026-04-14-api-index-missing-input-dir-404.md` с описанием сценария и проверок.

## Как работает итоговое решение

Тест отправляет `POST /index` с несуществующим `input_dir` и проверяет:

- `HTTP 404`;
- точный `detail` с проблемным путём;
- отсутствие созданного index-файла.

Так поведение `/index` фиксируется от регрессии на уровне API-контракта.

## Почему эти изменения нельзя было смешивать с другими

Если смешать этот тест с CORS или с `input_dir is not a directory`, пропадёт прозрачность: станет непонятно, какой именно failure mode защищает commit и что именно сломалось при будущем откате.

## Какие файлы изменены

- `backend/tests/test_api.py`
- `docs/commit-notes/2026-04-14-api-index-missing-input-dir-404.md`

## Какие проверки запущены

- `python3 -m unittest backend.tests.test_api.ApiTests.test_index_endpoint_returns_404_for_missing_input_dir`

## Результат проверки

Тест прошёл успешно и подтвердил детерминированное `404`-поведение `/index` для отсутствующей директории.

## Что осталось вне этого коммита

- отдельный regression-тест и note для local demo CORS;
- README и `docs/ARCHITECTURE_RU.md` sync для frontend demo;
- старый незакоммиченный шум в note `2026-04-14-api-index-file-input-dir-400.md`, который не должен переписывать историю задним числом.

## Следующий логичный маленький шаг

Отдельно зафиксировать local demo CORS regression coverage для `GET /health` с `Origin: http://127.0.0.1:5173`.
