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
- [`2026-04-14-cli-page-aware-source-rendering-regression.md`](./2026-04-14-cli-page-aware-source-rendering-regression.md) - regression-проверка того, что CLI показывает `page N` в блоке `Sources:` для чанка с page metadata
- [`2026-04-14-cli-non-paged-source-rendering-regression.md`](./2026-04-14-cli-non-paged-source-rendering-regression.md) - regression-проверка корректного рендеринга источников без страниц в CLI
- [`2026-04-14-cli-tie-order-regression.md`](./2026-04-14-cli-tie-order-regression.md) - regression-проверка стабильного порядка источников в CLI при равных retrieval score
- [`2026-04-14-evaluation-dataset-smoke-hardening.md`](./2026-04-14-evaluation-dataset-smoke-hardening.md) - усиление smoke-check для evaluation dataset: проверка ожидаемого источника и честного отказа на Q10
- [`2026-04-14-frontend-vite-scaffold.md`](./2026-04-14-frontend-vite-scaffold.md) - добавление минимального frontend-каркаса на React + TypeScript + Vite и подготовка typed API-слоя
- [`2026-04-14-frontend-demo-page.md`](./2026-04-14-frontend-demo-page.md) - реализация одностраничного frontend-demo с действиями health/index/ask и рендерингом grounded-ответа
- [`2026-04-14-api-cors-for-local-demo.md`](./2026-04-14-api-cors-for-local-demo.md) - минимальная CORS-настройка FastAPI для локального frontend-demo и regression-тест заголовка origin
- [`2026-04-14-docs-sync-for-frontend-demo.md`](./2026-04-14-docs-sync-for-frontend-demo.md) - синхронизация README и архитектурной документации с текущим frontend demo flow
- [`2026-04-14-final-verification-and-next-step.md`](./2026-04-14-final-verification-and-next-step.md) - финальный прогон проверок сессии и фиксация следующего маленького шага в NEXT_STEP
- [`2026-04-14-agent-support-files-baseline.md`](./2026-04-14-agent-support-files-baseline.md) - добавление практичных agent-support файлов (SONNET/playbook/bugfix workflow/project map/review template)
- [`2026-04-14-frontend-ask-readable-error-block.md`](./2026-04-14-frontend-ask-readable-error-block.md) - улучшение user-facing отображения ошибок `/ask` во frontend: статус + detail вместо сырого текста
- [`2026-04-14-api-index-missing-input-dir-404.md`](./2026-04-14-api-index-missing-input-dir-404.md) - защита `/index` от несуществующего `input_dir` с явным 404 и узким API regression test
- [`2026-04-14-api-index-file-input-dir-400.md`](./2026-04-14-api-index-file-input-dir-400.md) - защита `/index` от случая, когда `input_dir` существует, но указывает на файл, с явным 400 и узким API regression test
- [`2026-04-14-pdf-loader-missing-extractor-error.md`](./2026-04-14-pdf-loader-missing-extractor-error.md) - явный failure mode для `.pdf` без настроенного extractor: читаемое сообщение и focused loader regression test
- [`2026-04-14-frontend-index-informative-errors.md`](./2026-04-14-frontend-index-informative-errors.md) - улучшение информативности ошибок `/index` во фронтенде: согласованность с `/ask` и рендеринг деталей от бэкенда

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
