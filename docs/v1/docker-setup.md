# Запуск приложения в Docker

## Обзор

Приложение развертывается с использованием Docker Compose и состоит из следующих сервисов:
- **fastapi**: Основное приложение на FastAPI
- **postgres**: База данных PostgreSQL
- **rabbitmq**: Брокер сообщений RabbitMQ
- **celery**: Worker для асинхронной обработки задач
- **flower**: Веб-интерфейс для мониторинга Celery задач

## Структура файлов

```
docker/
├── fastapi/
│   ├── Dockerfile
│   ├── app.sh
│   ├── fastapi.env
│   └── fastapi.env.example
├── postgres/
│   ├── postgres.env
│   └── postgres.env.example
└── rabbitmq/
    ├── rabbitmq.conf
    ├── rabbitmq.env
    └── rabbitmq.env.example
```

## Запуск приложения

### Предварительные требования
- Docker и Docker Compose установлены
- Настроены файлы окружения (скопированы .env.example в .env)

### Команды запуска

```bash
# Сборка и запуск всех сервисов
docker-compose up --build

# Запуск в фоновом режиме
docker-compose up -d --build

# Остановка сервисов
docker-compose down

# Полное удаление
docker compose down -v --rmi local --remove-orphans

# Просмотр логов
docker-compose logs -f fastapi
docker-compose logs -f celery

# Пересборка конкретного сервиса
docker-compose up --build fastapi
```

## Volumes

- **fastapi_data**: Хранит данные приложения (загруженные файлы, логи)
- **postgres_data**: Хранит данные PostgreSQL
- **rabbitmq_data**: Хранит данные RabbitMQ

## Мониторинг и отладка

### Flower (мониторинг Celery)
- URL: http://localhost:5555
- Предоставляет информацию о задачах, воркерах, статистику

### RabbitMQ Management
- URL: http://localhost:15672
- Логин/пароль: из rabbitmq.env


См. также: [Настройки приложения](app-settings.md), [База данных](database.md)
