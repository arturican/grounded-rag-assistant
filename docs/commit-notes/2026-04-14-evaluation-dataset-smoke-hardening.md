# Commit: evaluation dataset smoke hardening

## Цель шага

Усилить текущий smoke-check для evaluation corpus так, чтобы он проверял не только наличие ответа, но и минимальную grounded-точность по источнику и честный отказ на заведомо отсутствующий факт.

## Почему этот шаг выделен отдельно

Это самостоятельный regression-пакет на уровне dataset smoke checks. Его нельзя смешивать ни с runtime-фиксами answer flow, ни с frontend/demo серией: здесь меняются только тестовые ожидания и документация для локальной проверки evaluation corpus.

## Какое состояние репозитория было до этого

До этого в `backend/tests/test_evaluation_dataset.py` был только базовый smoke-path: индексировать `sample_docs/text_only` и убедиться, что billing-вопрос возвращает ожидаемый факт. Но тест не закреплял источник ответа и не проверял вопрос Q10 из `docs/EVALUATION_DATASET.md`, который должен завершаться grounded refusal.

## Что изменено

- В `backend/tests/test_evaluation_dataset.py` добавлена проверка, что billing-вопрос ссылается на `support_playbook.txt`.
- В тот же модуль добавлен отдельный smoke-test на Q10: вопрос про travel reimbursement limit должен завершаться insufficient-context ответом без `Sources:`.
- В `docs/EVALUATION_DATASET.md` в секцию Suggested local verification добавлена CLI-команда для Q10.

## Как работает итоговое решение

Smoke-набор по-прежнему остаётся лёгким:

- индексирует только `sample_docs/text_only`;
- проверяет, что grounded billing-answer содержит и ожидаемый факт, и ожидаемый источник;
- проверяет, что unrelated question из Q10 не проходит как ложноположительный grounded answer.

## Почему эти изменения нельзя было смешивать с другими

Этот шаг касается только regression-слоя вокруг evaluation dataset. Его нельзя было смешивать с runtime-фиксом grounded refusal, потому что тогда один commit одновременно менял бы и тестовую цель, и механизм, по которому тест начинает проходить.

## Какие файлы изменены

- `backend/tests/test_evaluation_dataset.py`
- `docs/EVALUATION_DATASET.md`
- `docs/commit-notes/2026-04-14-evaluation-dataset-smoke-hardening.md`

## Какие проверки запущены

- `python3 -m unittest backend.tests.test_evaluation_dataset -v`
- `python3 -m unittest backend.tests.test_cli -v`

## Результат проверки

Оба набора прошли успешно. Новый smoke-test закрепил honest refusal для Q10, а существующий billing-scenario теперь дополнительно контролирует source attribution.

## Что осталось вне этого коммита

- agent-support документы;
- frontend scaffold/demo и связанный docs sync;
- незакоммиченные API/docs изменения для local demo (`/index` missing dir, CORS, README/architecture sync).

## Следующий логичный маленький шаг

Разобрать и зафиксировать doc-only пакет agent support files отдельным коммитом, не смешивая его с runtime или frontend изменениями.
