# Кастомный API-проект

Этот проект представляет собой шаблон API на базе FastAPI, PostgreSQL, Redis, Loki, Prometheus и Grafana. Он был изменен для уникальности и отличается от стандартных шаблонов.

## Сервисы

Проект состоит из следующих сервисов:
* `db_postgres`: База данных PostgreSQL для хранения данных приложения.
* `api_server`: Основной сервис API, написанный на FastAPI.
* `redis_cache`: Redis для кеширования данных.
* `metrics_server`: Prometheus для сбора метрик.
* `log_storage`: Loki для хранения логов.
* `monitoring_dashboard`: Grafana для визуализации метрик и логов.
* `log_collector`: Promtail для отправки логов в Loki.

## Запуск проекта

1.  **Настройка окружения**: Создайте файл `.env` в корневом каталоге и добавьте переменные окружения, как указано в `.env.example`.
2.  **Запуск Docker Compose**: В корневом каталоге выполните следующую команду:
    ```bash
    docker-compose up -d --build
    ```
3.  **Доступ к сервисам**:
    * API: http://localhost:8008
    * Grafana: http://localhost:3005
    * Prometheus: http://localhost:9095

## Структура проекта