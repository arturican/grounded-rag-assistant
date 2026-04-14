# Commit: add local demo CORS regression coverage

## Цель шага

Закрепить local demo CORS-поведение отдельным API regression test и note, чтобы browser-based frontend не сломался незаметно при будущих правках API слоя.

## Почему этот шаг выделен отдельно

CORS для local demo — это отдельный transport-layer contract. Его нельзя смешивать с `/index` validation или README/architecture sync: это другой пользовательский failure mode и другая причина регрессии.

## Какое состояние репозитория было до этого

К моменту этого коммита `CORSMiddleware` с локальными Vite origin уже был включён в `backend/app/api.py`, но в истории ещё не было отдельного узкого теста и note, явно фиксирующих именно этот контракт.

## Что изменено

- В `backend/tests/test_api.py` добавлен тест `test_health_allows_local_frontend_origin`.
- Добавлена note `docs/commit-notes/2026-04-14-api-cors-for-local-demo.md`.

## Как работает итоговое решение

Тест делает `GET /health` с заголовком `Origin: http://127.0.0.1:5173` и проверяет, что API возвращает `access-control-allow-origin` с тем же origin. Это защищает локальный browser-demo от тихого отката CORS-настроек.

## Почему эти изменения нельзя было смешивать с другими

Если этот тест смешать с `/index`-ошибками или docs sync, станет труднее понять, что именно откатилось: input validation, browser access или документация. Один transport contract — один commit.

## Какие файлы изменены

- `backend/tests/test_api.py`
- `docs/commit-notes/2026-04-14-api-cors-for-local-demo.md`

## Какие проверки запущены

- `python3 -m unittest backend.tests.test_api.ApiTests.test_health_allows_local_frontend_origin`

## Результат проверки

Тест прошёл успешно и подтвердил, что local frontend origin получает ожидаемый CORS-заголовок.

## Что осталось вне этого коммита

- README и `docs/ARCHITECTURE_RU.md` sync для frontend demo;
- stale noise в изменении старой note `2026-04-14-api-index-file-input-dir-400.md`, который не нужно тащить в новую историю.

## Следующий логичный маленький шаг

Синхронизировать README и архитектурную документацию с текущим frontend demo flow и уже работающими local demo API-contracts.
