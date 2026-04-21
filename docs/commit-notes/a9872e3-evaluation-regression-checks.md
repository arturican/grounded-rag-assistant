# `a9872e3` - evaluation regression checks

## Что появилось

В проект добавили детерминированные regression-тесты для двух самых хрупких мест RAG-пайплайна: ранжирования retrieval-результатов и сборки grounded-ответа. Основные изменения лежат в [backend/tests/test_retrieval.py](/home/art/project/grounded-rag-assistant/backend/tests/test_retrieval.py), [backend/tests/test_answering.py](/home/art/project/grounded-rag-assistant/backend/tests/test_answering.py) и обновлённом [docs/NEXT_STEP.md](/home/art/project/grounded-rag-assistant/docs/NEXT_STEP.md).

## Как это работает

Для retrieval используется специальный `FixedEvaluationEmbeddingProvider`, который возвращает заранее заданные векторы по тексту. За счёт этого тест не зависит ни от внешних моделей, ни от случайности, а проверяет именно порядок ранжирования: нужный чанк должен оказаться выше отвлекающих. Для answer layer отдельный regression-тест проверяет, что в итоговый ответ попадают только верхние чанки и что лишний контекст не протекает в результат.

## Зачем это нужно

Обычные unit-тесты проверяют отдельные функции, но не всегда страхуют от тихой деградации поведения. Этот коммит фиксирует важные пользовательские ожидания в виде устойчивых сценариев: retrieval должен отдавать самый релевантный источник первым, а answering layer должен строить ответ только из выбранного контекста. Это первый шаг к repeatable quality checks, о которых говорит Phase 9.
