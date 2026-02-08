from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Local file-based storage (JSON)
TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api", methods=["GET"])
def welcome():
    return jsonify({
        "message": "Welcome to To-Do App API",
        "version": "1.0.0",
        "endpoints": {
            "get_all_tasks": "GET /tasks",
            "get_task": "GET /tasks/<task_id>",
            "create_task": "POST /tasks",
            "update_task": "PUT /tasks/<task_id>",
            "delete_task": "DELETE /tasks/<task_id>"
        }
    })

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    if not data.get("title"):
        return jsonify({"error": "Title is required"}), 400
    tasks = load_tasks()
    task_id = max([task["id"] for task in tasks], default=0) + 1
    new_task = {
        "id": task_id,
        "title": data["title"],
        "description": data.get("description", ""),
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    if "completed" in data:
        task["completed"] = data["completed"]
    if "title" in data:
        task["title"] = data["title"]
    if "description" in data:
        task["description"] = data["description"]
    save_tasks(tasks)
    return jsonify(task)

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(tasks)
    return jsonify({"message": "Task deleted"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
