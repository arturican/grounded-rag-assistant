# Commit: add practical agent support docs baseline

## Цель шага

Добавить в репозиторий минимальный, но практичный набор agent-support документов, чтобы следующие проходы по маленьким шагам были воспроизводимыми и единообразными.

## Почему этот шаг выделен отдельно

Это полностью doc-only пакет. Он не должен смешиваться ни с API bugfix, ни с evaluation smoke, ни с frontend/demo серией, потому что меняет только способ работы агента с репозиторием, а не само пользовательское поведение проекта.

## Какое состояние репозитория было до этого

В репозитории был `AGENTS.md`, но не было:

- отдельного `SONNET.md`;
- проект-специфичных playbook/workflow/map документов;
- места для кратких agent notes;
- review template, ориентированного на findings и docs drift.

## Что изменено

- Добавлен `SONNET.md` с краткой картой проекта и рабочими правилами.
- Добавлены `docs/AI_AGENT_PLAYBOOK.md`, `docs/AI_BUGFIX_WORKFLOW.md`, `docs/AI_PROJECT_MAP.md`.
- Добавлен `docs/agent-notes/README.md`.
- Обновлён `docs/reviews/TEMPLATE.md` под формат findings: Critical, Correctness, Missing Tests, Docs Drift, Suggestions.

## Как работает итоговое решение

Новые документы не влияют на runtime. Они задают операционный каркас:

- как выбирать следующий шаг;
- как отличать баг от допустимого упрощения;
- как оформлять review findings;
- где хранить краткие промежуточные заметки между шагами.

## Почему эти изменения нельзя было смешивать с другими

Если смешать эти документы с кодовыми изменениями, commit history потеряет прозрачность: станет непонятно, что относится к продуктовой логике, а что только к process/tooling слою для агентов и ревью.

## Какие файлы изменены

- `SONNET.md`
- `docs/AI_AGENT_PLAYBOOK.md`
- `docs/AI_BUGFIX_WORKFLOW.md`
- `docs/AI_PROJECT_MAP.md`
- `docs/agent-notes/README.md`
- `docs/reviews/TEMPLATE.md`
- `docs/commit-notes/2026-04-14-agent-support-files-baseline.md`

## Какие проверки запущены

- Ручная проверка содержимого документов на согласованность с `AGENTS.md`, текущей структурой `backend/`, `frontend/` и `docs/`.

## Результат проверки

Документы согласованы с текущей структурой проекта и не требуют runtime-запуска. Несоответствий с основным `AGENTS.md` по workflow или целям репозитория не найдено.

## Что осталось вне этого коммита

- frontend scaffold/demo и связанный docs sync;
- незакоммиченные API/docs изменения для local demo (`/index` missing dir, CORS, README/architecture sync).

## Следующий логичный маленький шаг

Разобрать frontend/demo серию, начиная с минимального frontend scaffold без generated build-артефактов.
