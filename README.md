# To-Do App v1.0

A simple Flask-based To-Do application that allows users to create, read, update, and delete tasks. The application is containerized using Docker and uses a local JSON file for storing tasks.

## Features

- **CRUD Operations**: Create, read, update, and delete tasks
- **Local Storage**: Data is stored in a JSON file
- **Containerized**: Fully containerized using Docker and Docker Compose
- **RESTful API**: Easy-to-use REST API for managing tasks
- **Development Ready**: Includes hot-reload for development
- **Interactive Dashboard**: Real-time statistics with visual charts
- **Task Statistics**: Progress bar and task distribution graph
- **Wave Animation**: Beautiful animated ocean waves background

## Project Structure

```
/cc302-cicd-pip-lines
|-- /app
|   |-- app.py (Flask application)
|   |-- requirements.txt (Python dependencies)
|   |-- Dockerfile (Docker configuration)
|   |-- docker-compose.yml (Docker Compose configuration)
|   |-- tasks.json (Task storage)
|   |-- /static (Static files)
|   |-- /templates (HTML templates)
|   |-- README.md (API documentation)
|-- README.md (This file)
```

## Prerequisites

- Docker and Docker Compose installed
- Python 3.9+ (for local development without Docker)
- Git

## Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd cc302-cicd-pip-lines
   ```

2. Build and run the application:
   ```bash
   cd app
   docker-compose up --build
   ```

3. Access the application at [http://localhost:5000](http://localhost:5000)

### Using Docker Directly

1. Build the Docker image:
   ```bash
   cd app
   docker build -t todo-app:latest .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 -v $(pwd):/app todo-app:latest
   ```

### Local Development (without Docker)

1. Install dependencies:
   ```bash
   cd app
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. The app will be accessible at [http://localhost:5000](http://localhost:5000)

## API Endpoints

All endpoints return JSON responses.

### Get All Tasks
- **Endpoint**: `GET /tasks`
- **Response**: Array of all tasks
- **Example**:
  ```bash
  curl http://localhost:5000/tasks
  ```

### Get Task by ID
- **Endpoint**: `GET /tasks/<task_id>`
- **Response**: Single task object or error
- **Example**:
  ```bash
  curl http://localhost:5000/tasks/1
  ```

### Create New Task
- **Endpoint**: `POST /tasks`
- **Request Body**:
  ```json
  {
    "title": "Task title",
    "description": "Task description (optional)"
  }
  ```
- **Response**: Created task object with ID
- **Example**:
  ```bash
  curl -X POST http://localhost:5000/tasks \
    -H "Content-Type: application/json" \
    -d '{"title": "My first task", "description": "Do something important"}'
  ```

### Update Task
- **Endpoint**: `PUT /tasks/<task_id>`
- **Request Body** (all fields optional):
  ```json
  {
    "title": "Updated title",
    "description": "Updated description",
    "completed": true
  }
  ```
- **Response**: Updated task object
- **Example**:
  ```bash
  curl -X PUT http://localhost:5000/tasks/1 \
    -H "Content-Type: application/json" \
    -d '{"completed": true}'
  ```

### Delete Task
- **Endpoint**: `DELETE /tasks/<task_id>`
- **Response**: Success message
- **Example**:
  ```bash
  curl -X DELETE http://localhost:5000/tasks/1
  ```

## Data Storage

Tasks are stored in `app/tasks.json` with the following structure:

```json
[
  {
    "id": 1,
    "title": "Example task",
    "description": "Task description",
    "completed": false,
    "created_at": "2024-02-08T10:30:45.123456"
  }
]
```

## Environment Variables

The application supports the following environment variables in `docker-compose.yml`:

- `FLASK_APP`: Set to `app.py`
- `FLASK_ENV`: Set to `development` (for development) or `production`

## Testing

You can test the API using `curl`:

```bash
# Get all tasks
curl http://localhost:5000/tasks

# Create a task
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Docker", "description": "Master containerization"}'

# Update a task
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete a task
curl -X DELETE http://localhost:5000/tasks/1
```

## Docker Hub Deployment

To deploy this application on Docker Hub:

1. Build the image:
   ```bash
   docker build -t yourusername/todo-app:latest .
   ```

2. Log in to Docker Hub:
   ```bash
   docker login
   ```

3. Push the image:
   ```bash
   docker push yourusername/todo-app:latest
   ```

4. Pull and run from any system:
   ```bash
   docker pull yourusername/todo-app:latest
   docker run -p 5000:5000 yourusername/todo-app:latest
   ```

## GitHub Setup

To push this repository to GitHub:

```bash
git init
git add .
git commit -m "Initial commit: To-Do app with Docker"
git branch -M main
git remote add origin https://github.com/yourusername/todo-app.git
git push -u origin main
```

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify the port mapping in `docker-compose.yml`:
```yaml
ports:
  - "8000:5000"  # Change to 8000:5000
```

### Tasks File Not Found
The `tasks.json` file is automatically created on first run. If you want to reset it:
```bash
rm app/tasks.json
docker-compose down
docker-compose up --build
```

### Volume Permission Issues
If you have permission issues with the mounted volume, ensure the container user has write access to the tasks.json file.

## Development

To extend this application:

1. Add new routes to `app/app.py`
2. Update `requirements.txt` with new dependencies
3. Rebuild the Docker image for changes to take effect

## License

This project is open source and available for educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or issues.
