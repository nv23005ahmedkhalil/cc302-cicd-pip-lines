# To-Do App - API Documentation

This is the Flask backend for the To-Do application. It provides a RESTful API for managing tasks with full CRUD functionality.

## Running the App

### Using Docker Compose
```bash
docker-compose up --build
```

### Using Python Directly
```bash
pip install -r requirements.txt
python app.py
```

The app will start on `http://localhost:5000`

## API Endpoints

### 1. Get All Tasks
```
GET /tasks
```

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "title": "Learn Flask",
    "description": "Master Flask framework",
    "completed": false,
    "created_at": "2024-02-08T10:30:45.123456"
  }
]
```

### 2. Get Single Task
```
GET /tasks/<task_id>
```

**Response (200 OK)**:
```json
{
  "id": 1,
  "title": "Learn Flask",
  "description": "Master Flask framework",
  "completed": false,
  "created_at": "2024-02-08T10:30:45.123456"
}
```

**Response (404 Not Found)**:
```json
{
  "error": "Task not found"
}
```

### 3. Create Task
```
POST /tasks
```

**Request Body**:
```json
{
  "title": "Task title",
  "description": "Optional description"
}
```

**Response (201 Created)**:
```json
{
  "id": 1,
  "title": "Task title",
  "description": "Optional description",
  "completed": false,
  "created_at": "2024-02-08T10:30:45.123456"
}
```

**Response (400 Bad Request)**:
```json
{
  "error": "Title is required"
}
```

### 4. Update Task
```
PUT /tasks/<task_id>
```

**Request Body** (all fields optional):
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

**Response (200 OK)**:
```json
{
  "id": 1,
  "title": "Updated title",
  "description": "Updated description",
  "completed": true,
  "created_at": "2024-02-08T10:30:45.123456"
}
```

**Response (404 Not Found)**:
```json
{
  "error": "Task not found"
}
```

### 5. Delete Task
```
DELETE /tasks/<task_id>
```

**Response (200 OK)**:
```json
{
  "message": "Task deleted"
}
```

**Response (404 Not Found)**:
```json
{
  "error": "Task not found"
}
```

## cURL Examples

### Get all tasks
```bash
curl http://localhost:5000/tasks
```

### Create a task
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

### Update a task
```bash
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### Delete a task
```bash
curl -X DELETE http://localhost:5000/tasks/1
```

## Data Storage

Tasks are persisted in `tasks.json`. The file is automatically created on first run and stores all tasks as a JSON array.

## Dependencies

- **Flask 2.1.1**: Lightweight web framework
- Python 3.9+

See `requirements.txt` for full dependencies.

## Docker

The application is fully containerized. See the `Dockerfile` for the container configuration.

### Building the Docker Image
```bash
docker build -t todo-app:latest .
```

### Running the Container
```bash
docker run -p 5000:5000 -v $(pwd):/app todo-app:latest
```

## Development

The app runs in development mode with `debug=True`, which provides:
- Auto-reload on code changes
- Interactive debugger
- Detailed error messages

For production deployment, disable debug mode by modifying `app.py`:
```python
app.run(debug=False)
```

## Error Handling

All API responses follow a consistent format:
- **Success**: HTTP status codes 200, 201
- **Client Error**: HTTP status codes 400, 404
- **Server Error**: HTTP status code 500

Errors include an `error` field with a descriptive message.
