# Архитектура приложения

## Диаграмма компонентов системы

```mermaid
graph TB
    subgraph "Клиент"
        Client[HTTP Client]
    end

    subgraph "API Layer"
        FastAPI[FastAPI Application]
        Validation[File Validation]
        Router[Transcriptions Router]
    end

    subgraph "Business Logic"
        Service[TranscriptionService]
        Repo[TranscriptionsRepo]
        Storage[LocalStorage]
        AI[OpenAiClient<br/>• Transcribe Audio<br/>• Answer Questions]
    end

    subgraph "Async Processing"
        Celery[Celery Worker]
        Task[transcribe_audio Task]
    end

    subgraph "Infrastructure"
        Postgres[(PostgreSQL)]
        RabbitMQ[(RabbitMQ)]
        Files[(Local Files)]
    end

    Client --> FastAPI
    FastAPI --> Validation
    Validation --> Router
    Router --> Service

    Service --> Repo
    Service --> Storage
    Service --> AI

    Service -.-> Celery
    Celery --> Task

    Task --> AI
    Task --> Repo

    Repo --> Postgres
    Storage --> Files
    Celery -.-> RabbitMQ

    style FastAPI fill:#e1f5fe
    style Service fill:#f3e5f5
    style Celery fill:#fff3e0
    style Postgres fill:#e8f5e8
    style RabbitMQ fill:#ffebee
```

## Процесс обработки транскрибации

```mermaid
sequenceDiagram
    participant Client
    participant FastAPI
    participant Storage
    participant DB
    participant Celery
    participant AI

    Client->>FastAPI: POST /transcriptions (audio file)
    FastAPI->>FastAPI: Validate file
    FastAPI->>Storage: Save audio file
    Storage-->>FastAPI: file_path
    FastAPI->>DB: Create transcription record
    DB-->>FastAPI: transcription_id
    FastAPI->>Celery: Start async task
    FastAPI-->>Client: 202 Accepted + transcription_id

    Celery->>DB: Get transcription record
    DB-->>Celery: transcription data
    Celery->>AI: Process audio transcription
    AI-->>Celery: transcription text
    Celery->>DB: Update transcription record

    Client->>FastAPI: GET /transcriptions/{id}
    FastAPI->>DB: Get transcription status
    DB-->>FastAPI: transcription data
    FastAPI->>Celery: Check task status
    Celery-->>FastAPI: task state
    FastAPI-->>Client: transcription status/result

    Client->>FastAPI: POST /transcriptions/{id}/questions (question)
    FastAPI->>DB: Get transcription with text
    DB-->>FastAPI: transcription data
    FastAPI->>AI: Answer question based on transcription
    AI-->>FastAPI: answer text
    FastAPI-->>Client: question + answer
```

## Диаграмма потоков данных

```mermaid
flowchart TD
    A[Аудиофайл] --> B{Валидация}
    B -->|Invalid| C[Ошибка 400]
    B -->|Valid| D[Сохранение в Storage]

    D --> E[Запись в БД]
    E --> F[ID транскрибации]

    F --> G[Запуск Celery Task]
    G --> H{Обработка AI}

    H -->|Success| I[Обновление БД]
    H -->|Failure| J[Логирование ошибки]

    I --> K[Транскрибация готова]

    F --> L[Проверка статуса]
    L --> M{Статус задачи}

    M -->|PENDING/STARTED| N[Статус: в обработке]
    M -->|SUCCESS| O[Возврат результата]
    M -->|FAILURE| P[Возврат ошибки]

    K --> O

    O --> Q[Задавание вопросов]
    Q --> R{Есть вопрос?}
    R -->|Да| S[Отправка в AI]
    S --> T[Получение ответа]
    T --> U[Возврат ответа]
    U --> R
    R -->|Нет| V[Конец]


    style Q fill:#e8f5e8
    style S fill:#fff3e0
```

См. также: [Обзор проекта](README.md), [API Endpoints](api-endpoints.md)
