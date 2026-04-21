# Commit: frontend build typing baseline fix

## Цель исправления

Убрать предсуществующие frontend-ошибки типизации, из-за которых `npm run build` не проходил, и вернуть проекту чистую базовую сборку перед следующим packaging-шагом.

## Как была обнаружена проблема

Проблема воспроизводилась прямым запуском `npm run build` в каталоге `frontend/`.
После поднятия локального `node/npm` в окружении сборка завершалась ошибками TypeScript:

- `src/api.ts(3,34): error TS2339: Property 'env' does not exist on type 'ImportMeta'.`
- `src/main.tsx(4,8): error TS2882: Cannot find module or type declarations for side-effect import of './styles.css'.`

## Почему это реальная проблема

Frontend уже использует стандартные для Vite конструкции:

- `import.meta.env.VITE_API_BASE_URL` для чтения переменной окружения;
- side-effect import `./styles.css` в entrypoint.

Без Vite client type declarations TypeScript не знает ни про `ImportMeta.env`, ни про CSS-импорты, поэтому production build падает ещё до шага `vite build`.

## Что изменено

Добавлен один минимальный файл `frontend/src/vite-env.d.ts` со ссылкой на `vite/client`.

Также обновлены:

- `docs/NEXT_STEP.md` — следующий маленький шаг теперь сформулирован как backend-only Docker image;
- `docs/commit-notes/README.md` — добавлена ссылка на эту заметку.

## Как работает исправление

`vite/client` добавляет ambient type declarations для frontend-проекта Vite, включая:

- `ImportMeta.env`;
- поддержку импортов статических ассетов и CSS.

После этого существующий код в `frontend/src/api.ts` и `frontend/src/main.tsx` начинает корректно типизироваться без изменения бизнес-логики и без вмешательства в UI.

## Почему решение сделано именно так

Это самый узкий и стандартный фикс для Vite + TypeScript:

- не меняет API-контракт;
- не трогает backend;
- не требует dependency changes;
- не разводит рефакторинг в `api.ts` или `main.tsx`, где сам runtime-код уже был корректным.

## Какие файлы изменены

- `frontend/src/vite-env.d.ts`
- `docs/NEXT_STEP.md`
- `docs/commit-notes/README.md`
- `docs/commit-notes/2026-04-14-frontend-build-typing-baseline-fix.md`

## Какие проверки запущены

- `cd /home/artur/project/grounded-rag-assistant/frontend && npm run build`

## Результат проверки

До исправления сборка падала на двух TypeScript-ошибках.
После добавления `vite/client` declarations `npm run build` проходит успешно.

## Ограничения

- Шаг специально не затрагивает Docker, packaging и backend.
- Исправление покрывает только реальные причины текущего падения frontend build.
- Локально для проверки понадобился временный Node runtime в окружении, потому что в исходном shell `npm` отсутствовал.

## Следующий логичный маленький шаг

Добавить `Dockerfile.backend` и задокументировать точные команды `docker build`, `docker run` и проверку `/health` без перехода пока к `docker-compose` и frontend containerization.
