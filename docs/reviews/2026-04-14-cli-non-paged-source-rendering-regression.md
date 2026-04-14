# 2026-04-14-cli-non-paged-source-rendering-regression.md

## 1. Проверенный шаг (Reviewed Step)
Добавить CLI-тест на регрессию, который проверяет, что рендеринг источников без метаданных страниц сохраняет формат без упоминания страниц.

## 2. Список проверенных файлов (Files Inspected)
- `backend/tests/test_cli.py`
- `docs/NEXT_STEP.md`

## 3. Что выглядит корректно (What looks correct)
- Добавлен тест `test_run_cli_renders_non_paged_sources_without_page_suffix_regression`.
- Тест правильно настраивает временную директорию и индекс.
- Проверка `assertFalse(any("page None" in line for line in rendered_lines))` гарантирует отсутствие некорректного вывода.
- Ожидаемая строка источника сформирована верно: `- {source_path} ({source_path}::page-none::chunk-0)`.

## 4. Возможные риски и ошибки (Risks & Bugs)
- **Correctness**: Зависимость от `fastapi` в `backend/tests/test_api.py` всё ещё сломана в текущем окружении, но это не касается данного теста.
- **Suggestion**: В будущем можно добавить проверку на `page 0`, чтобы исключить другие неверные форматы.

## 5. Проверка тестов (Test Verification)
- Все тесты в `backend.tests.test_cli` прошли успешно (6 тестов).
- Общий прогон тестов (за исключением API) подтверждает стабильность.

## 6. Соответствие документации (Docs Alignment)
- `docs/NEXT_STEP.md` обновлён на следующий шаг (проверка детерминизма при равных скорах).
- Файл `GEMINI.md` и другие руководства созданы/обновлены.

## 7. Рекомендуемый следующий шаг (Recommended Next Small Step)
Реализовать проверку детерминированного порядка при равных similarity score на уровне CLI, как указано в обновлённом `docs/NEXT_STEP.md`.
