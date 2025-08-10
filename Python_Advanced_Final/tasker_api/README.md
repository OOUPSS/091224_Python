# FastAPI Task Manager

![Project Dashboard](https://github.com/OOUPSS/091224_Python/blob/main/fstp.png?raw=true)

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://travis-ci.org/)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org)

## Project Overview

**FastAPI Task Manager** is a robust and scalable task management service built with **FastAPI**. It provides a **RESTful API** for performing CRUD operations on tasks, supports real-time service health monitoring, and is ready for deployment using **Docker**. The project is designed for high performance, real-time notifications, and comprehensive monitoring and logging.

### Key Features
- 🚀 **High Performance**: Leverages FastAPI for asynchronous request handling.
- 🔔 **Real-Time Notifications**: Integrated WebSocket support for instant updates.
- 🛠️ **Reliable Database**: Uses Alembic for seamless database migrations.
- 📊 **Monitoring & Logging**: Integrated with Prometheus, Grafana, and Loki for metrics and centralized logging.

## Technology Stack
- **Backend**: Python 3.9+
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Database Migrations**: Alembic
- **Containerization**: Docker & Docker Compose
- **Monitoring**: Prometheus & Grafana
- **Logging**: Loki

---

## Getting Started

### Prerequisites
- Docker
- Docker Compose
- Python 3.9+ (optional, for local development without Docker)

### Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone git clone https://github.com/OOUPSS/091224_Python.git
   cd 091224_Python/Python_Advanced_Final/tasker_api
   ```

2. **Configure Environment Variables**:
   - Copy `.env.example` to `.env` and update it with your configuration (e.g., database credentials).

3. **Launch Services**:
   ```bash
   docker-compose up --build
   ```

4. **Run Database Migrations**:
   ```bash
   ./migrate.sh
   ```

5. **Access the Service**:
   - The API is available at `http://localhost:8000`.
   - API documentation is available at `http://localhost:8000/docs`.

## API Endpoints

### 1. **Create a Task**
- **Method**: `POST /tasks/`
- **Description**: Creates a new task with a required `title` field and optional `description` and `status` fields.
- **Request Body**:
  ```json
  {
    "title": "Write report",
    "description": "Prepare monthly report for management.",
    "status": "in_progress"
  }
  ```
- **Responses**:
  - **201 Created**:
    ```json
    {
      "id": 1,
      "title": "Write report",
      "status": "in_progress",
      "created_at": "2025-08-10T15:19:00Z"
    }
    ```
  - **422 Unprocessable Entity**:
    ```json
    {
      "detail": "Request body validation failed"
    }
    ```

### 2. **List All Tasks**
- **Method**: `GET /tasks/`
- **Description**: Retrieves a list of all tasks in the system.
- **Response**:
  - **200 OK**:
    ```json
    [
      {
        "id": 1,
        "title": "Write report",
        "status": "in_progress",
        "created_at": "2025-08-10T15:19:00Z"
      },
      {
        "id": 2,
        "title": "Schedule meeting",
        "status": "pending",
        "created_at": "2025-08-10T15:20:00Z"
      }
    ]
    ```

### 3. **Get Task by ID**
- **Method**: `GET /tasks/{task_id}`
- **Description**: Retrieves details of a specific task by its unique ID.
- **Responses**:
  - **200 OK**:
    ```json
    {
      "id": 1,
      "title": "Write report",
      "status": "in_progress",
      "created_at": "2025-08-10T15:19:00Z"
    }
    ```
  - **404 Not Found**:
    ```json
    {
      "detail": "Task with ID 1 not found"
    }
    ```

### 4. **Update a Task**
- **Method**: `PUT /tasks/{task_id}`
- **Description**: Fully updates an existing task by its ID. All fields except `id` and `created_at` must be provided.
- **Request Body**:
  ```json
  {
    "title": "Reschedule meeting",
    "description": "Coordinate with team for a new time.",
    "status": "done"
  }
  ```
- **Responses**:
  - **200 OK**:
    ```json
    {
      "id": 1,
      "title": "Reschedule meeting",
      "status": "done",
      "created_at": "2025-08-10T15:19:00Z"
    }
    ```
  - **404 Not Found**:
    ```json
    {
      "detail": "Task with ID 1 not found"
    }
    ```

### 5. **Delete a Task**
- **Method**: `DELETE /tasks/{task_id}`
- **Description**: Deletes a task by its unique ID.
- **Responses**:
  - **204 No Content**: Task successfully deleted (no response body).
  - **404 Not Found**:
    ```json
    {
      "detail": "Task with ID 1 not found"
    }
    ```

## Monitoring & Logging

- **Prometheus**: Access metrics at `http://localhost:9090`.
- **Grafana**: Visualize data at `http://localhost:3000`.
- **Loki**: Aggregates logs for centralized logging.

## Project Structure

```bash
fastapi-task-manager/
├── alembic/                    # Database migration scripts
├── grafana/                    # Grafana configuration
├── src/                        # Application source code
│   ├── api/                    # API-related code
│   │   ├── dependencies/       # Dependency injection
│   │   ├── endpoints/          # API route definitions
│   │   ├── middleware/         # Custom middleware
│   │   └── schemas/            # Pydantic schemas
│   ├── core/                   # Core configuration and utilities
│   ├── db/                     # Database setup and models
│   ├── exceptions/             # Custom exception handlers
│   ├── loggers/                # Logging configuration
│   ├── repositories/           # Data access layer
│   ├── services/               # Business logic
│   ├── tests/                  # Unit and integration tests
│   ├── utils/                  # Utility functions
│   └── websockets/             # WebSocket handlers
├── .dockerignore               # Docker ignore file
├── .env                        # Environment variables
├── .gitignore                  # Git ignore file
├── alembic.ini                 # Alembic configuration
├── docker-compose.override.yml # Override for Docker Compose
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker configuration
├── loki-config.yaml            # Loki configuration
├── main.py                     # Application entry point
├── migrate.sh                  # Database migration script
├── prometheus.yml              # Prometheus configuration
├── promtail-config.yaml        # Promtail configuration
├── pytest.ini                  # Pytest configuration
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
```

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
