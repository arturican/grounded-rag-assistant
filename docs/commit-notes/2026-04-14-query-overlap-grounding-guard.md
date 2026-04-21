# Commit: guard grounded answers with query-term overlap

## Цель шага

Сделать honest-refusal поведение устойчивее в локальной сборке с `FakeEmbeddingProvider`, где высокий similarity score сам по себе ещё не гарантирует смысловую релевантность ответа.

## Почему этот шаг выделен отдельно

В рабочем дереве уже лежал пакет `evaluation dataset smoke hardening`, но его ключевой тест на Q10 падал: вопрос про travel reimbursement limit приводил к ответу из нерелевантных operational chunks. Это не проблема самого smoke-теста, а отдельный bug в grounded answer flow, поэтому сначала нужен маленький runtime-фикс.

## Какое состояние репозитория было до этого

`build_grounded_answer(...)` принимал решение только по `min_score`. Для fake-embedding этого оказалось недостаточно: длинный unrelated query мог получить очень высокий cosine similarity и пройти в user-facing answer, даже если в retrieved chunks не было ни одного meaningful term из вопроса.

## Что изменено

- В `backend/app/answering.py` добавлена дополнительная проверка meaningful overlap между query и выбранными retrieved chunks.
- В `backend/app/cli.py` и `backend/app/api.py` query теперь передаётся в `build_grounded_answer(...)`.
- В `backend/tests/test_answering.py` добавлен focused unit test на scenario "high score without query overlap".

## Как работает итоговое решение

После прохождения score-порога answer layer дополнительно извлекает значимые термы из query и retrieved text, отбрасывая короткие токены и базовые stopwords. Если пересечения нет, ответ считается insufficient-context и возвращается стандартный grounded refusal без sources.

Это не заменяет retrieval, а служит узкой защитой на границе user-facing answer flow для текущего deterministic fake-embedding режима.

## Почему эти изменения нельзя было смешивать с другими

Этот шаг исправляет именно логику grounded refusal. Его нельзя было смешивать с evaluation smoke hardening, потому что иначе commit с тестами одновременно менял бы и тестовую цель, и runtime-поведение, скрывая реальную причину падения.

## Какие файлы изменены

- `backend/app/answering.py`
- `backend/app/cli.py`
- `backend/app/api.py`
- `backend/tests/test_answering.py`
- `docs/commit-notes/README.md`
- `docs/commit-notes/2026-04-14-query-overlap-grounding-guard.md`

## Какие проверки запущены

- `python3 -m unittest backend.tests.test_answering -v`
- `python3 -m unittest backend.tests.test_cli -v`
- `python3 -m unittest backend.tests.test_api -v`
- `python3 -m unittest backend.tests.test_evaluation_dataset -v`

## Результат проверки

Все перечисленные наборы прошли успешно. Новый unit test подтвердил refusal при отсутствии query-term overlap, а evaluation smoke для Q10 перестал давать ложноположительный grounded answer.

## Что осталось вне этого коммита

- отдельный коммит на `evaluation dataset smoke hardening` в `backend/tests/test_evaluation_dataset.py` и `docs/EVALUATION_DATASET.md`;
- agent-support документы;
- frontend scaffold/demo и связанный docs sync;
- незакоммиченные API/docs изменения для local demo (`/index` missing dir, CORS, README/architecture sync).

## Следующий логичный маленький шаг

Теперь можно честно зафиксировать `evaluation dataset smoke hardening` отдельным коммитом: ожидаемый источник для billing-вопроса и честный refusal на Q10 уже реально подтверждаются тестами.
