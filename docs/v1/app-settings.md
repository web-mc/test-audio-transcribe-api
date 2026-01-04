# Настройки приложения и переменные окружения

## Обзор

Приложение использует систему конфигурации на основе Pydantic Settings для управления настройками через переменные окружения. Все настройки разделены на логические группы.

## Основные настройки приложения (AppSettings)

### app_dir
- **Тип**: Path
- **Значение по умолчанию**: Родительская директория файла конфигурации
- **Описание**: Базовая директория приложения.

### log_dir
- **Тип**: Path
- **Значение по умолчанию**: `app_dir / "logs"`
- **Описание**: Директория для хранения лог-файлов.

### production
- **Тип**: bool
- **Значение по умолчанию**: False
- **Описание**: Флаг производственной среды. Влияет на уровень логирования.

### allowed_extensions
- **Тип**: tuple
- **Значение по умолчанию**: `(".mp3", ".wav")`
- **Описание**: Допустимые расширения аудиофайлов для загрузки.

### max_file_size
- **Тип**: int
- **Значение по умолчанию**: `25 * 1024 * 1024` (25 MB)
- **Описание**: Максимальный размер загружаемого файла в байтах.

### loglevel (свойство)
- **Тип**: int
- **Описание**: Уровень логирования (INFO в продакшене, DEBUG в разработке).

## Настройки Gunicorn (GunicornSettings)

### hostname
- **Тип**: str
- **Значение по умолчанию**: `gethostname()`
- **Описание**: Имя хоста сервера.

### host
- **Тип**: str
- **Значение по умолчанию**: `gethostbyname(hostname)`
- **Описание**: IP-адрес хоста.

### API_PORT
- **Тип**: int
- **Значение по умолчанию**: 8000
- **Описание**: Порт для запуска API сервера.

### reload
- **Тип**: bool
- **Значение по умолчанию**: `not app_settings.production`
- **Описание**: Автоматическая перезагрузка сервера при изменениях (отключена в продакшене).

## Настройки базы данных (DatabaseSettings)

### POSTGRES_USER
- **Тип**: str
- **Значение по умолчанию**: "postgres"
- **Описание**: Имя пользователя базы данных.

### POSTGRES_PASSWORD
- **Тип**: SecretStr
- **Значение по умолчанию**: "postgres"
- **Описание**: Пароль пользователя базы данных.

### POSTGRES_HOST
- **Тип**: str
- **Значение по умолчанию**: "localhost"
- **Описание**: Хост базы данных.

### POSTGRES_PORT
- **Тип**: int
- **Значение по умолчанию**: 5432
- **Описание**: Порт базы данных.

### POSTGRES_SCHEMA
- **Тип**: str
- **Значение по умолчанию**: "public"
- **Описание**: Схема базы данных.

### POSTGRES_DB
- **Тип**: str
- **Значение по умолчанию**: "postgres"
- **Описание**: Имя базы данных.

### conn_string (свойство)
- **Тип**: URL
- **Описание**: Полная строка подключения к базе данных (генерируется автоматически).

## Настройки RabbitMQ (RabbitMQSettings)

### RABBITMQ_DEFAULT_USER
- **Тип**: str
- **Значение по умолчанию**: "guest"
- **Описание**: Имя пользователя RabbitMQ.

### RABBITMQ_DEFAULT_PASS
- **Тип**: SecretStr
- **Значение по умолчанию**: "guest"
- **Описание**: Пароль пользователя RabbitMQ.

### RABBITMQ_DEFAULT_VHOST
- **Тип**: str
- **Значение по умолчанию**: "vhost"
- **Описание**: Виртуальный хост RabbitMQ.

### RABBITMQ_DEFAULT_HOST
- **Тип**: str
- **Значение по умолчанию**: "localhost"
- **Описание**: Хост RabbitMQ.

### RABBITMQ_DEFAULT_PORT
- **Тип**: int
- **Значение по умолчанию**: 5672
- **Описание**: Порт RabbitMQ.

### broker_url (свойство)
- **Тип**: str
- **Описание**: URL брокера сообщений (генерируется автоматически).

## Настройки AI (AiSettings)

### AI_BASE_URL
- **Тип**: str
- **Обязательная**: Да
- **Описание**: Базовый URL для API искусственного интеллекта.

### AI_API_KEY
- **Тип**: SecretStr
- **Обязательная**: Да
- **Описание**: API ключ для доступа к сервису AI.

### AI_AUDIO_MODEL
- **Тип**: str
- **Обязательная**: Да
- **Описание**: Модель AI для транскрибации аудио.

### AI_TEXT_MODEL
- **Тип**: str
- **Обязательная**: Да
- **Описание**: Модель AI для обработки текстовых запросов.

## Примеры файлов окружения

### docker/fastapi/fastapi.env
```
# Производственные настройки
PRODUCTION=true

# Настройки AI (примеры)
AI_BASE_URL=https://api.openai.com/v1
AI_API_KEY=your_openai_api_key_here
AI_AUDIO_MODEL=whisper-1
AI_TEXT_MODEL=gpt-3.5-turbo

# Настройки Gunicorn
API_PORT=8000
```

### docker/postgres/postgres.env
```
# Настройки PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=audio_transcriptions
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_SCHEMA=public
```

### docker/rabbitmq/rabbitmq.env
```
# Настройки RabbitMQ
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=secure_rabbitmq_password
RABBITMQ_DEFAULT_VHOST=/
RABBITMQ_DEFAULT_HOST=rabbitmq
RABBITMQ_DEFAULT_PORT=5672
```

## Безопасность

- Все секретные значения (пароли, API ключи) хранятся как `SecretStr` и не логируются.
- Переменные окружения имеют префиксы для группировки (`POSTGRES_`, `RABBITMQ_DEFAULT_`, `AI_`).
- Файлы окружения не должны попадать в систему контроля версий.

См. также: [Запуск в Docker](docker-setup.md), [База данных](database.md)
