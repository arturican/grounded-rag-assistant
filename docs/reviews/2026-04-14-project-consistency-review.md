# 2026-04-14-project-consistency-review.md

## 1. Проверенный шаг (Reviewed Step)
Целостная проверка проекта после реализации Phase 9 (CLI-регрессии).

## 2. Список проверенных файлов (Files Inspected)
- `backend/app/retrieval.py`
- `backend/tests/test_cli.py`
- `docs/NEXT_STEP.md`
- `docs/commit-notes/README.md`

## 3. Что выглядит корректно (What looks correct)
- Детерминированный порядок retrieval-результатов при равных скорах (`score`, `chunk_index`, `chunk_id`) реализован в `retrieval.py`.
- Все 57 логических тестов (включая CLI регрессии для tie-breaking и non-paged sources) проходят.
- История коммитов в `commit-notes/README.md` соответствует реальному состоянию репозитория.

## 4. Возможные риски и ошибки (Risks & Bugs)
- **Correctness (Fixed)**: Обнаружен `zip` без `strict=True` в `retrieval.py` (метод `add_chunks`). Исправлено для безопасности типов.
- **Docs Drift (Fixed)**: `docs/NEXT_STEP.md` содержал уже выполненную задачу. Обновлен на следующий этап (Evaluation Dataset).
- **Environment**: Тесты API (`test_api.py`) падают из-за отсутствия `fastapi` в текущем окружении. Это внешняя проблема, не связанная с качеством кода.

## 5. Проверка тестов (Test Verification)
- 58 тестов запущено: 57 OK, 1 ERROR (API).
- `test_run_cli_returns_tied_sources_in_stable_order_regression` проходит успешно.

## 6. Соответствие документации (Docs Alignment)
- `ARCHITECTURE_RU.md` и `PROJECT_BRIEF.md` актуальны.
- `ROADMAP.md` соблюдается.

## 7. Рекомендуемый следующий шаг (Recommended Next Small Step)
Сформировать демонстрационный набор документов (`sample_docs/`) и вопросов для оценки (`docs/EVALUATION_DATASET.md`), как указано в обновленном `NEXT_STEP.md`.
