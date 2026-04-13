# `451ed52` - FastAPI layer

## Что появилось

Добавлен HTTP-слой в [backend/app/api.py](/home/art/project/grounded-rag-assistant/backend/app/api.py), тесты эндпоинтов в [backend/tests/test_api.py](/home/art/project/grounded-rag-assistant/backend/tests/test_api.py), зависимости FastAPI в [pyproject.toml](/home/art/project/grounded-rag-assistant/pyproject.toml) и команды запуска API в [README.md](/home/art/project/grounded-rag-assistant/README.md).

## Как это работает

FastAPI переиспользует уже существующий локальный пайплайн вместо отдельной новой логики. Эндпоинт `/health` проверяет доступность приложения, `/index` индексирует документы в локальный JSON-индекс, а `/ask` загружает этот индекс, выполняет retrieval и возвращает grounded-ответ со структурированными источниками.

## Зачем это нужно

После этого коммита проект становится удобнее для интеграции: к нему уже можно обращаться не только через CLI, но и по HTTP. Это мост между учебным локальным прототипом и будущим UI или внешними клиентами.

## Примечание по истории

Сообщение коммита в git получилось сокращённым до `Add` из-за локального поведения оболочки во время коммита. Эта заметка фиксирует фактический смысл коммита, чтобы история проекта оставалась понятной при чтении.
