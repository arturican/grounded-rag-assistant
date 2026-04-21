# AI Project Map

## Карта модулей

- `backend/app/models.py` - базовые контракты `DocumentChunk` и `RetrievedChunk`.
- `backend/app/chunking.py` - нормализация и разбиение текста на чанки.
- `backend/app/loaders.py` - загрузка документов в нормализованный формат.
- `backend/app/ingestion.py` - сборка chunk-моделей из загруженного документа.
- `backend/app/embeddings.py` - провайдер эмбеддингов (сейчас fake/deterministic).
- `backend/app/retrieval.py` - индексация и top-k поиск по эмбеддингам.
- `backend/app/answering.py` - сборка grounded-ответа и форматирование источников.
- `backend/app/index_store.py` - сериализация/десериализация индекса.
- `backend/app/cli.py` - пользовательский CLI (`index`, `ask`).
- `backend/app/api.py` - HTTP-обертка (`/health`, `/index`, `/ask`).
- `frontend/src/api.ts` - клиент API.
- `frontend/src/types.ts` - TS-контракты API.
- `frontend/src/App.tsx` - UI состояния и отображение результатов.

## Кто за что отвечает

- **Loaders + Ingestion**: превращают файлы в валидные чанки с metadata.
- **Embeddings + Retrieval**: находят релевантные чанки.
- **Answering**: формирует ответ строго из retrieval-результата.
- **CLI/API**: транспортный слой, не место для новой бизнес-логики.
- **Frontend**: demo-рендер API контракта.

## Основные потоки данных

1. `index`:
   `load_document` -> `build_document_chunks` -> `add_chunks` -> `save_index`
2. `ask`:
   `load_index` -> `search` -> `build_grounded_answer` -> render (CLI/API/Frontend)

## Какие файлы трогать для типовых задач

- Ошибка формата источников: `backend/app/answering.py`, `backend/tests/test_answering.py`, `backend/tests/test_cli.py`.
- Ошибка ранжирования retrieval: `backend/app/retrieval.py`, `backend/tests/test_retrieval.py`.
- Ошибка API-контракта: `backend/app/api.py`, `backend/tests/test_api.py`, `frontend/src/types.ts`, `frontend/src/api.ts`.
- Ошибка отображения UI: `frontend/src/App.tsx`, `frontend/src/styles.css`.
- Изменение пользовательского workflow: `README.md`, `docs/ARCHITECTURE_RU.md`, `docs/NEXT_STEP.md`.
