# Commit: add backend-only Docker image

## Цель шага

Добавить backend-only Docker image, чтобы FastAPI API можно было поднять в чистом и повторяемом контейнере до перехода к полной multi-service упаковке.

## Почему этот шаг выделен отдельно

Это изолированный packaging-шаг. Его нельзя смешивать с frontend containerization или application logic: здесь меняется только способ запуска уже существующего backend API.

## Какое состояние репозитория было до этого

Проект уже запускался локально через системный Python и `uvicorn`, а `docs/NEXT_STEP.md` прямо требовал backend-only container packaging как следующий минимальный шаг. При этом в репозитории ещё не было `Dockerfile.backend` и точных команд для container verification.

## Что изменено

- Добавлен `Dockerfile.backend` на базе `python:3.12-slim`.
- В `README.md` добавлены точные команды:
  - `docker build -f Dockerfile.backend -t grounded-rag-assistant-backend .`
  - `docker run --rm -p 8000:8000 --name grounded-rag-assistant-backend grounded-rag-assistant-backend`
  - `curl http://127.0.0.1:8000/health`
- `docs/NEXT_STEP.md` обновлён на следующий маленький шаг: минимальный local multi-service compose stack.

## Как работает итоговое решение

Контейнер:

- использует лёгкий Python base image;
- устанавливает только runtime-зависимости FastAPI API;
- копирует `backend/` в `/app`;
- запускает `uvicorn backend.app.api:app --host 0.0.0.0 --port 8000`.

В результате backend API можно собрать и запустить без локального Python-окружения проекта.

## Почему эти изменения нельзя было смешивать с другими

Этот шаг касается только backend packaging. Если смешать его с compose, frontend containerization или runtime-правками, будет неясно, что именно требуется для первого воспроизводимого container start API.

## Какие файлы изменены

- `Dockerfile.backend`
- `README.md`
- `docs/NEXT_STEP.md`
- `docs/commit-notes/README.md`
- `docs/commit-notes/2026-04-14-backend-docker-image.md`

## Какие проверки запущены

- `docker build -f Dockerfile.backend -t grounded-rag-assistant-backend .`
- `docker run --rm -d -p 8000:8000 --name grounded-rag-assistant-backend-test grounded-rag-assistant-backend`
- `docker exec grounded-rag-assistant-backend-test python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/health').read().decode())"`
- `docker stop grounded-rag-assistant-backend-test`

## Результат проверки

- `docker build` прошёл успешно.
- Контейнер успешно стартовал и `uvicorn` поднял API на `0.0.0.0:8000`.
- `/health` внутри running container вернул `{"status":"ok"}`.
- Прямой `curl` с хоста из текущего sandbox не смог достучаться до published port, поэтому финальная health-проверка была выполнена через `docker exec` внутри контейнера. Сам контейнерный API при этом работал корректно.

## Что осталось вне этого коммита

- frontend containerization;
- `docker-compose.yml` или другой multi-service orchestration;
- любые application-logic изменения.

## Следующий логичный маленький шаг

Добавить минимальный local demo compose stack, который поднимает вместе backend container и frontend demo без production orchestration scope.
