# To-Do List – Project Overview

## Description

This project is a simple To-Do List application built with Streamlit and SQLite, using SQLAlchemy as the ORM layer.

The application allows users to:
- add new tasks,
- view all tasks,
- mark tasks as completed or incomplete,
- delete individual tasks,
- clear the entire task list,
- sort tasks by date, name, or status.

The database is automatically created on first run and stored locally.
The app can be run using Docker.

## Database Structure (ERD)

#### The application uses a single database table *tasks*.

```bash
erDiagram
    TASKS {
        int id
        string description
        boolean done
        datetime created_at
    }
```

### Table:

| Column      | Type     | Description        |
|-------------|----------|--------------------|
| id          | Integer  | Primary key        |
| description | String   | Task content       |
| done        | Bool     | Completion status  |
| created_at  | DataTime | Creation timestamp |

## Tests

The project includes:

- Database tests – verify CRUD operations

- Smoke test – ensures Streamlit app starts correctly

# Running the Project

### To start:

```bash
docker-compose up --build
```

##### Then open: [http://localhost:3000](http://localhost:3000)

### To stop:

```bash
docker-compose down
```
