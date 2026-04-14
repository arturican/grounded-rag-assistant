# Commit: frontend vite scaffold

## Цель шага

Добавить в репозиторий недостающий frontend runtime scaffold для React + TypeScript + Vite, чтобы уже существующий demo-компонент мог собираться и запускаться как отдельный клиентский пакет.

## Почему этот шаг выделен отдельно

Это инфраструктурный frontend-шаг: package/config/entry/api/types/build-игнорирование. Его нельзя смешивать с README/architecture sync, API CORS или evaluation smoke, потому что он завершает именно файловый каркас `frontend/`.

## Какое состояние репозитория было до этого

В истории уже был frontend-компонент `frontend/src/App.tsx` и последующий fix `vite-env.d.ts`, но в рабочем дереве отсутствовали остальные исходники и конфигурационные файлы, без которых frontend нельзя было ни собрать, ни запустить как отдельный Vite-пакет.

## Что изменено

- Добавлены `frontend/package.json`, `frontend/package-lock.json`, `frontend/index.html`.
- Добавлены `frontend/tsconfig.json`, `frontend/tsconfig.app.json`, `frontend/tsconfig.node.json`, `frontend/vite.config.ts`.
- Добавлены `frontend/src/main.tsx`, `frontend/src/api.ts`, `frontend/src/types.ts`, `frontend/src/styles.css`.
- Добавлен `frontend/.gitignore` и в него включены generated build-артефакты: `node_modules`, `dist`, `*.tsbuildinfo`, `vite.config.js`, `vite.config.d.ts`.

## Как работает итоговое решение

- `main.tsx` монтирует уже существующий `App`.
- `api.ts` содержит тонкий typed-клиент для `/health`, `/index`, `/ask`.
- `types.ts` фиксирует frontend-контракт под текущие API response/request поля.
- Vite/TypeScript-конфиг делает frontend отдельной воспроизводимой сборочной единицей.

## Почему эти изменения нельзя было смешивать с другими

Этот шаг не меняет пользовательскую документацию и не добавляет backend-поведение. Если смешать его с docs sync или API CORS, станет непонятно, что именно требуется для самого существования frontend-пакета, а что уже относится к локальному demo flow поверх него.

## Какие файлы изменены

- `frontend/.gitignore`
- `frontend/index.html`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/src/api.ts`
- `frontend/src/main.tsx`
- `frontend/src/styles.css`
- `frontend/src/types.ts`
- `frontend/tsconfig.app.json`
- `frontend/tsconfig.json`
- `frontend/tsconfig.node.json`
- `frontend/vite.config.ts`
- `docs/commit-notes/2026-04-14-frontend-vite-scaffold.md`

## Какие проверки запущены

- `PATH=/tmp/node22/current/bin:$PATH /tmp/node22/current/bin/npm install`
- `PATH=/tmp/node22/current/bin:$PATH /tmp/node22/current/bin/npm run build`

## Результат проверки

Frontend-зависимости установились успешно, а production build прошёл без ошибок. Generated build-файлы после проверки остаются вне git благодаря `.gitignore`.

## Что осталось вне этого коммита

- README и `docs/ARCHITECTURE_RU.md` для local demo flow;
- note и возможная синхронизация по frontend demo/documentation;
- backend local-demo тесты и notes для CORS и `/index` missing-dir.

## Следующий логичный маленький шаг

Синхронизировать пользовательскую документацию и архитектурное описание с уже рабочим local frontend demo, не смешивая это с backend regression coverage.
