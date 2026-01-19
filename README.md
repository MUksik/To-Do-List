# To-Do List – Project Overview


## Description
This project is a simple To-Do List application built with Streamlit and SQLite, using SQLAlchemy as the ORM layer.
The application allows users to:
- add new tasks,
- view all tasks,
- mark tasks as completed or incomplete,
- delete individual tasks,
- clear the entire task list,
- filter tasks by status,
- sort tasks by date or name.
The database is automatically created on first run and stored locally.
The app can be run using Docker.


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


## Tests
- ### Database tests
  #### Located in `tests/test_db.py`, they check:
  - basic CRUD operations
  - ignoring empty or whitespace-only tasks
  - trimming spaces from task descriptions
  - safe behavior when task ID does not exist
  - correct order of returned tasks
- ### Internationalization (i18n) tests
  #### Located in `tests/test_i18n.py`, they verify:
  - correct Polish and English translations
  - fallback to default language
  - returning the key if translation is missing
  - handling None as language value
- ### Smoke test
  #### Checks whether the Streamlit application starts correctly and does not crash during startup.
### To run tests:
```bash
docker-compose run --rm tdl pytest -q
```


## Database Structure (ERD)
#### The application uses a single database table *tasks*.
```js
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
| done        | Boolean  | Completion status  |
| created_at  | DataTime | Creation timestamp |