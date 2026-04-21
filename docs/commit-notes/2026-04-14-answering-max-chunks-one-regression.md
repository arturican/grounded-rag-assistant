# Commit: test: cover answering max_chunks one regression

## Что было целью шага

Целью шага было зафиксировать важный контракт answer layer: если `build_grounded_answer(...)` вызывается с `max_chunks=1`, итоговый ответ и список источников должны использовать только самый верхний retrieved chunk. Это важно для grounded-поведения, потому что answer layer не должен случайно подтягивать дополнительный контекст, когда вызывающий код явно ограничил число чанков одним.

## Почему это следующий маленький шаг

Это следующий логичный маленький шаг после retrieval-regression тестов. Retrieval уже фиксирует порядок найденных чанков, а теперь нужно проверить, что answer layer корректно уважает ограничение `max_chunks`. Шаг очень небольшой: один новый unit-тест без изменения архитектуры и без вмешательства в production-код.

## Что изменено

- `backend/tests/test_answering.py`
  Добавлен regression-тест `test_build_grounded_answer_regression_limits_answer_to_top_chunk_when_max_chunks_is_one`.
- `docs/NEXT_STEP.md`
  Обновлён следующий маленький шаг: теперь предлагается CLI-regression тест на page-aware rendering источников.
- `docs/commit-notes/2026-04-14-answering-max-chunks-one-regression.md`
  Добавлена подробная русскоязычная заметка по этому коммиту.
- `docs/commit-notes/README.md`
  В индекс заметок добавлена ссылка на новую запись.

## Как работает новый тест

Тест создаёт небольшой список из двух `RetrievedChunk`, уже отсортированных по релевантности:

- первый чанк `chunk-top` имеет более высокий `score=0.97`;
- второй чанк `chunk-lower` имеет более низкий `score=0.91`.

После этого вызывается:

```python
answer = build_grounded_answer(chunks, min_score=0.1, max_chunks=1)
```

Дальше тест явно проверяет весь нужный контракт:

- `used_context` равно `True`;
- `answer.answer` содержит только текст верхнего чанка;
- текст второго чанка не попадает в финальный ответ;
- в `answer.sources` ровно один элемент;
- этот единственный source указывает именно на верхний chunk (`chunk-top`, `policies.md`, `page=2`).

Такой тест не зависит ни от retrieval, ни от CLI, ни от API. Он проверяет только ответственный слой: deterministic answer assembly.

## Почему решение сделано именно так

Решение повторяет уже существующий стиль тестов в `backend/tests/test_answering.py`:

- используются реальные `RetrievedChunk`;
- значения `score` заданы явно;
- вызывается настоящий `build_grounded_answer(...)`;
- assertions написаны простым и читаемым образом.

Я не менял [backend/app/answering.py](/home/artur/project/grounded-rag-assistant/backend/app/answering.py), потому что новый тест сразу проходит на текущей реализации. Это соответствует правилу проекта: не менять application code, если тест не выявил реальный баг.

## Какие тесты запущены

```bash
cd /home/artur/project/grounded-rag-assistant
python3 -m unittest backend.tests.test_answering -v
```

## Результат проверки

Все answering-тесты прошли успешно. Проверено, что:

- существующие сценарии honest failure и multi-chunk assembly не сломаны;
- новый regression-тест на `max_chunks=1` проходит;
- answer layer действительно ограничивает и текст ответа, и список источников только верхним чанком.

## Ограничения

Тест проверяет только поведение answer layer на уже отсортированном списке `RetrievedChunk`. Он не валидирует сам retrieval-порядок и не проверяет пользовательский рендеринг этого результата в CLI или API. Это нормальное ограничение для unit-level regression шага.

## Следующий логичный маленький шаг

Следующим маленьким шагом логично добавить CLI-regression тест на page-aware rendering источников: проверить, что если source имеет `page`, CLI печатает человекочитаемый суффикс `page N` в блоке `Sources:`.
