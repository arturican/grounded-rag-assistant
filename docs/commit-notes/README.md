# Commit Notes

Этот каталог нужен не для формальной отчётности, а для нормального чтения истории проекта человеком.
Здесь мы раскладываем развитие репозитория по маленьким коммитам и объясняем каждый шаг простыми словами:

- что именно добавили;
- как это работает в коде;
- зачем этот шаг был нужен именно в этот момент.

## Как читать историю

1. Начинайте сверху вниз по логике пайплайна: от каркаса репозитория к ingestion, retrieval, answer layer, CLI и API.
2. Если интересен конкретный файл или слой, откройте заметку к коммиту и потом сразу соответствующий файл из репозитория.
3. Если в рабочем дереве есть новые изменения без коммита, их здесь ещё не будет: раздел описывает только уже зафиксированные шаги.

## Основная цепочка кодовых коммитов

- [`3a938d2-init-project.md`](./3a938d2-init-project.md) - стартовая структура репозитория и правила работы
- [`7ff5f15-core-retrieval-chunk-models.md`](./7ff5f15-core-retrieval-chunk-models.md) - базовые модели данных для чанков и retrieval
- [`88751bb-whitespace-normalization-helper.md`](./88751bb-whitespace-normalization-helper.md) - нормализация текста перед chunking
- [`660c46b-paragraph-splitting-helper.md`](./660c46b-paragraph-splitting-helper.md) - разбиение текста по абзацам
- [`43d2c32-sliding-window-text-chunking.md`](./43d2c32-sliding-window-text-chunking.md) - fallback-окна для длинных абзацев
- [`9d9477a-txt-document-loader.md`](./9d9477a-txt-document-loader.md) - загрузка `.txt`
- [`9fb1d61-markdown-document-loader.md`](./9fb1d61-markdown-document-loader.md) - загрузка `.md`
- [`b214a3f-document-loader-dispatch.md`](./b214a3f-document-loader-dispatch.md) - единая точка выбора document loader
- [`a24cec3-pdf-loader-contract.md`](./a24cec3-pdf-loader-contract.md) - контракт PDF-загрузчика и изоляция backend-парсера
- [`a85a500-embeddings-provider-interface.md`](./a85a500-embeddings-provider-interface.md) - интерфейс embedding provider
- [`5baa559-document-chunk-builder.md`](./5baa559-document-chunk-builder.md) - сборка `DocumentChunk` из загруженного документа
- [`7d68951-in-memory-retrieval-store.md`](./7d68951-in-memory-retrieval-store.md) - локальное in-memory retrieval-хранилище
- [`8b9d11d-grounded-answer-assembly.md`](./8b9d11d-grounded-answer-assembly.md) - детерминированная сборка grounded-ответа
- [`ffd8742-local-cli-vertical-slice.md`](./ffd8742-local-cli-vertical-slice.md) - первый рабочий CLI-срез
- [`451ed52-fastapi-layer.md`](./451ed52-fastapi-layer.md) - HTTP API поверх уже существующего локального пайплайна
- [`a9872e3-evaluation-regression-checks.md`](./a9872e3-evaluation-regression-checks.md) - детерминированные regression-проверки для retrieval и answer layer
- [`faf7f09-api-honest-failure-regression.md`](./faf7f09-api-honest-failure-regression.md) - regression-проверка честного отказа на уровне API и настройка порога для user-facing answer flow
- [`2026-04-14-cli-unrelated-query-regression.md`](./2026-04-14-cli-unrelated-query-regression.md) - regression-проверка честного отказа CLI на нерелевантный запрос к локальному индексу
- [`2026-04-14-retrieval-score-tie-regression.md`](./2026-04-14-retrieval-score-tie-regression.md) - regression-проверка детерминированного порядка retrieval-результатов при равных similarity score
- [`2026-04-14-answering-max-chunks-one-regression.md`](./2026-04-14-answering-max-chunks-one-regression.md) - regression-проверка того, что `max_chunks=1` оставляет в answer layer только верхний retrieved chunk

## Документационные коммиты, которые поясняют проект

- [`b0be41b-russian-commit-study-notes.md`](./b0be41b-russian-commit-study-notes.md) - запуск русскоязычного раздела с разбором истории по коммитам
- [`6158324-fastapi-commit-purpose-note.md`](./6158324-fastapi-commit-purpose-note.md) - пояснение смысла FastAPI-коммита с неудачным коротким сообщением в git
- [`753bb2c-russian-architecture-walkthrough.md`](./753bb2c-russian-architecture-walkthrough.md) - цельное архитектурное описание проекта на русском

## Как поддерживать раздел дальше

- После каждого нового маленького коммита добавляйте один новый markdown-файл в этот каталог.
- Используйте имя в формате `<short-sha>-<short-topic>.md`.
- Описывайте только то поведение и ту документацию, которые реально попали в коммит.
- Если коммит закрывает текущий шаг из `docs/NEXT_STEP.md`, сразу обновляйте `docs/NEXT_STEP.md` на следующий маленький шаг.
- Если сообщение коммита в git получилось слишком коротким или неудачным, это место можно использовать как человеческое пояснение, что на самом деле было сделано.
