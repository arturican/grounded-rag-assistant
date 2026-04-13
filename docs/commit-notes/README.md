# Commit Notes

Это учебный раздел с русскоязычными пояснениями по основным коммитам проекта.

Как читать:

1. Идите сверху вниз по истории.
2. В каждом файле есть три главных блока: что добавили, как это работает, зачем это нужно.
3. Если в рабочем дереве появились новые изменения, но коммит ещё не создан, их здесь пока не будет.

Основная цепочка коммитов:

- [`3a938d2-init-project.md`](./3a938d2-init-project.md) - инициализация репозитория и правил работы
- [`7ff5f15-core-retrieval-chunk-models.md`](./7ff5f15-core-retrieval-chunk-models.md) - базовые модели чанков
- [`88751bb-whitespace-normalization-helper.md`](./88751bb-whitespace-normalization-helper.md) - нормализация текста
- [`660c46b-paragraph-splitting-helper.md`](./660c46b-paragraph-splitting-helper.md) - разбиение по абзацам
- [`43d2c32-sliding-window-text-chunking.md`](./43d2c32-sliding-window-text-chunking.md) - оконный chunking длинных текстов
- [`9d9477a-txt-document-loader.md`](./9d9477a-txt-document-loader.md) - загрузка `.txt`
- [`9fb1d61-markdown-document-loader.md`](./9fb1d61-markdown-document-loader.md) - загрузка `.md`
- [`b214a3f-document-loader-dispatch.md`](./b214a3f-document-loader-dispatch.md) - единая точка выбора загрузчика
- [`a24cec3-pdf-loader-contract.md`](./a24cec3-pdf-loader-contract.md) - контракт загрузки PDF
- [`a85a500-embeddings-provider-interface.md`](./a85a500-embeddings-provider-interface.md) - интерфейс эмбеддингов
- [`5baa559-document-chunk-builder.md`](./5baa559-document-chunk-builder.md) - сборка чанков документа
- [`7d68951-in-memory-retrieval-store.md`](./7d68951-in-memory-retrieval-store.md) - локальное хранилище и поиск
- [`8b9d11d-grounded-answer-assembly.md`](./8b9d11d-grounded-answer-assembly.md) - сборка grounded-ответа
- [`ffd8742-local-cli-vertical-slice.md`](./ffd8742-local-cli-vertical-slice.md) - первый рабочий CLI-срез
- [`451ed52-fastapi-layer.md`](./451ed52-fastapi-layer.md) - HTTP API для текущего локального RAG-среза

Как поддерживать раздел дальше:

- после нового коммита добавляйте один новый markdown-файл в этот каталог;
- используйте имя в формате `<short-sha>-<short-topic>.md`;
- описывайте только реально попавшее в коммит поведение;
- если коммит меняет план проекта, синхронизируйте это с `docs/NEXT_STEP.md`.
