# Commit: docs sync for frontend demo

## Цель шага

Привести ключевую пользовательскую и архитектурную документацию в соответствие с текущим local demo flow после появления frontend-пакета и local-demo API поведения.

## Почему этот шаг выделен отдельно

Это чистый docs sync. Его нельзя смешивать ни с frontend scaffold, ни с API regression-тестами: здесь меняется только описание того, как проект запускать и как устроен текущий demo-срез.

## Какое состояние репозитория было до этого

К этому моменту в репозитории уже были frontend runtime files, demo-компонент и local-demo API contracts, но README и `docs/ARCHITECTURE_RU.md` ещё не описывали:

- наличие `frontend/`;
- фактический JSON index вместо FAISS в текущем runtime;
- локальные команды запуска frontend;
- роль frontend слоя в общей архитектуре;
- локальные CORS-origin для demo.

## Что изменено

- В `README.md`:
  - добавлен `frontend/` в карту репозитория;
  - уточнено текущее состояние хранилища (`local JSON index`);
  - добавлены команды `npm install`, `npm run dev`, `npm run build`;
  - добавлен `VITE_API_BASE_URL` override;
  - зафиксированы локальные CORS origin;
  - добавлены user-facing примечания про ошибки `/ask` и `/index`.
- В `docs/ARCHITECTURE_RU.md`:
  - добавлен frontend слой;
  - добавлена локальная CORS-настройка API;
  - цепочка зависимостей расширена до `... -> cli/api -> frontend`.

## Как работает итоговое решение

Runtime-код не меняется. Документация теперь отражает реальный demo-поток:

1. запустить FastAPI;
2. запустить frontend на Vite;
3. использовать UI для `/health`, `/index`, `/ask`;
4. при ошибках видеть ожидаемое поведение и в API, и в UI.

## Почему эти изменения нельзя было смешивать с другими

Если смешать docs sync с runtime-коммитами, история станет менее читаемой: непонятно, менялось ли поведение приложения или только описание того, как это поведение воспроизвести.

## Какие файлы изменены

- `README.md`
- `docs/ARCHITECTURE_RU.md`
- `docs/commit-notes/2026-04-14-docs-sync-for-frontend-demo.md`

## Какие проверки запущены

- `python3 -m unittest backend.tests.test_api -v`
- `PATH=/tmp/node22/current/bin:$PATH /tmp/node22/current/bin/npm run build`

## Результат проверки

API-набор прошёл успешно, frontend production build тоже прошёл. Документация синхронизирована с рабочим кодом и проверочными командами.

## Что осталось вне этого коммита

- missing study notes для уже существующих frontend/demo шагов (`frontend-demo-page`, `frontend-ask-readable-error-block`);
- final verification note как отдельный documentation-only след сессии.

## Следующий логичный маленький шаг

Добавить оставшиеся commit-study notes для уже завершённых frontend/demo шагов, чтобы `docs/commit-notes/README.md` не ссылался на отсутствующие файлы.
