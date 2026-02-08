from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
import re

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

@app.route("/modern", methods=["GET"])
def modern_app():
    return render_template("modern_app.html")

# NLP Task Parser
def parse_nlp_input(text):
    """Parse natural language input into task components"""
    result = {
        'title': text,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'time': '09:00',
        'priority': 'medium',
        'tags': []
    }
    
    # Extract priority (!!!, !!, !)
    if '!!!' in text or '!!!!' in text:
        result['priority'] = 'high'
        text = re.sub(r'!{2,}', '', text)
    elif '!!' in text:
        result['priority'] = 'high'
        text = re.sub(r'!!', '', text)
    elif '!' in text:
        result['priority'] = 'medium'
        text = re.sub(r'!', '', text)
    
    # Extract tags (#tag)
    tags = re.findall(r'#\w+', text)
    result['tags'] = [tag.replace('#', '') for tag in tags]
    text = re.sub(r'#\w+', '', text)
    
    # Extract time (at HH:MM or at 2pm)
    time_match = re.search(r'at (\d{1,2}):(\d{2})', text)
    if time_match:
        result['time'] = f"{int(time_match.group(1)):02d}:{time_match.group(2)}"
        text = re.sub(r'at \d{1,2}:\d{2}', '', text)
    else:
        time_match = re.search(r'at (\d{1,2})(?:am|pm)?', text)
        if time_match:
            hour = int(time_match.group(1))
            result['time'] = f"{hour:02d}:00"
            text = re.sub(r'at \d{1,2}(?:am|pm)?', '', text)
    
    # Extract date
    today = datetime.now()
    if 'tomorrow' in text:
        result['date'] = (today + timedelta(days=1)).strftime('%Y-%m-%d')
        text = re.sub(r'tomorrow', '', text)
    elif 'today' in text:
        result['date'] = today.strftime('%Y-%m-%d')
        text = re.sub(r'today', '', text)
    elif 'next week' in text:
        result['date'] = (today + timedelta(days=7)).strftime('%Y-%m-%d')
        text = re.sub(r'next week', '', text)
    elif 'next monday' in text.lower():
        days_until_monday = (7 - today.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        result['date'] = (today + timedelta(days=days_until_monday)).strftime('%Y-%m-%d')
        text = re.sub(r'next monday', '', text, flags=re.IGNORECASE)
    
    result['title'] = text.strip()
    return result

@app.route("/api", methods=["GET"])
def welcome():
    return jsonify({
        "message": "Welcome to TaskFlow Pro API",
        "version": "2.0.0",
        "endpoints": {
            "get_all_tasks": "GET /tasks",
            "get_task": "GET /tasks/<task_id>",
            "create_task": "POST /tasks",
            "update_task": "PUT /tasks/<task_id>",
            "delete_task": "DELETE /tasks/<task_id>",
            "parse_nlp": "POST /api/parse-nlp",
            "smart_schedule": "POST /api/smart-schedule",
            "my_day": "GET /api/my-day"
        }
    })

@app.route("/api/parse-nlp", methods=["POST"])
def parse_nlp():
    """Parse natural language input"""
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    parsed = parse_nlp_input(text)
    return jsonify(parsed)

@app.route("/api/smart-schedule", methods=["POST"])
def smart_schedule():
    """Auto-schedule tasks into next available free time"""
    data = request.get_json()
    tasks = load_tasks()
    
    # Get all existing tasks
    existing_tasks = tasks
    
    # Find next available time slot
    now = datetime.now()
    available_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
    
    # Simple scheduling: each task gets 60 minutes
    for task in existing_tasks:
        if task['date'] == available_time.strftime('%Y-%m-%d'):
            task_time = datetime.strptime(f"{task['date']} {task['time']}", '%Y-%m-%d %H:%M')
            available_time = max(available_time, task_time + timedelta(hours=1))
    
    return jsonify({
        'suggested_date': available_time.strftime('%Y-%m-%d'),
        'suggested_time': available_time.strftime('%H:%M')
    })

@app.route("/api/my-day", methods=["GET"])
def get_my_day():
    """Get today's tasks with intelligent suggestions"""
    tasks = load_tasks()
    today = datetime.now().strftime('%Y-%m-%d')
    
    today_tasks = [t for t in tasks if t.get('date') == today and not t.get('archived')]
    
    # Sort by priority and time
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    today_tasks.sort(key=lambda x: (priority_order.get(x.get('priority', 'low'), 3), x.get('time', '00:00')))
    
    # Calculate stats
    stats = {
        'total': len(today_tasks),
        'completed': len([t for t in today_tasks if t.get('completed')]),
        'high_priority': len([t for t in today_tasks if t.get('priority') == 'high']),
        'tasks': today_tasks
    }
    
    return jsonify(stats)

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
    today = datetime.now().isoformat().split('T')[0]
    new_task = {
        "id": task_id,
        "title": data["title"],
        "description": data.get("description", ""),
        "date": data.get("date", today),
        "time": data.get("time", "00:00"),
        "completed": False,
        "archived": False,
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
    if "archived" in data:
        task["archived"] = data["archived"]
    if "title" in data:
        task["title"] = data["title"]
    if "description" in data:
        task["description"] = data["description"]
    if "date" in data:
        task["date"] = data["date"]
    if "time" in data:
        task["time"] = data["time"]
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
