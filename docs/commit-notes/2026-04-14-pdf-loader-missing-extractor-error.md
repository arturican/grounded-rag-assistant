# Commit: make missing PDF extractor failure explicit

## Цель исправления

Сделать сбой при встрече `.pdf` без настроенного extractor более явным и читаемым, чтобы он не выглядел как абстрактный runtime failure без полезного контекста.

## Как была обнаружена проблема

Проблема пришла из аудита, после чего была перепроверена по текущему коду и локальному вызову `load_pdf_file` и `load_document`: при отсутствии extractor выбрасывался `RuntimeError` с коротким сообщением `pdf backend is unavailable`.

## Почему это реальная проблема

Такое сообщение говорит, что что-то сломалось вокруг PDF, но не объясняет сам failure mode. Когда индексация проходит по каталогу и упирается в конкретный PDF-файл, полезно явно увидеть, что backend не настроен именно потому, что extractor не был передан, и какой файл это вызвал.

## Что изменено

- В `backend/app/loaders.py` улучшено сообщение ошибки для случая `extractor is None`.
- Сообщение теперь сохраняет прежний смысл про недоступный backend, но добавляет явное указание на отсутствие configured extractor и на конкретный файл.
- В `backend/tests/test_loaders.py` добавлен ровно один focused test на точный текст ошибки для этого сценария.
- В `docs/NEXT_STEP.md` зафиксирован следующий маленький шаг после этого изменения.

## Как работает исправление

Если `load_pdf_file()` вызывается для существующего `.pdf`, но без `extractor`, loader теперь прерывается с детерминированным сообщением:

`pdf backend is unavailable: no extractor configured for file ...`

Так как `load_document()` для `.pdf` делегирует в `load_pdf_file()`, это же сообщение дойдёт и до более верхнего уровня ingestion/CLI flow.

## Почему решение сделано именно так

Это минимальный безопасный шаг:

- не меняет успешную загрузку PDF при наличии extractor;
- не трогает TXT/Markdown loaders;
- не требует реальной PDF-библиотеки;
- не меняет тип исключения и не ломает существующий контракт вызывающего кода;
- добавляет ровно один новый focused test вместо широкого рефакторинга.

## Какие файлы изменены

- `backend/app/loaders.py`
- `backend/tests/test_loaders.py`
- `docs/NEXT_STEP.md`
- `docs/commit-notes/README.md`
- `docs/commit-notes/2026-04-14-pdf-loader-missing-extractor-error.md`

## Какие тесты и проверки запущены

- `python3 -m unittest backend/tests/test_loaders.py -v`

## Результат проверки

Узкий набор `backend/tests/test_loaders.py` прошёл успешно; новый focused test подтвердил точное и читаемое сообщение ошибки для `.pdf` без extractor.

## Ограничения

- Этот коммит не добавляет реальный PDF parser/backend.
- Этот коммит не меняет frontend, API и общий ingestion flow поверх loader layer.
- Поведение по-прежнему основано на явной инъекции extractor, а не на default implementation.

## Следующий логичный маленький шаг

Сделать frontend-обработку ошибок `/index` такой же информативной, как у `/ask`, чтобы UI показывал backend status и detail вместо общего текста ошибки.
