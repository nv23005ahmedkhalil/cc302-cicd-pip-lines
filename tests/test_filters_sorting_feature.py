import os
import sys
from datetime import datetime, timedelta

import pytest

sys.path.insert(0, os.path.abspath("app"))
import app as app_module
from app import app as flask_app


@pytest.fixture
def client(tmp_path):
    flask_app.config["TESTING"] = True
    app_module.TASKS_FILE = str(tmp_path / "tasks.json")

    with flask_app.test_client() as client:
        yield client


def test_filters_and_sorting(client):
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    tasks = [
        {
            "title": "High urgent",
            "description": "priority item",
            "date": tomorrow,
            "priority": "high",
            "tags": ["work"],
        },
        {
            "title": "Medium today",
            "description": "active item",
            "date": today,
            "priority": "medium",
            "tags": ["home"],
        },
        {
            "title": "Low overdue",
            "description": "backlog",
            "date": yesterday,
            "priority": "low",
            "tags": ["finance"],
        },
    ]

    for payload in tasks:
        create = client.post("/tasks", json=payload)
        assert create.status_code == 201

    overdue = client.get("/tasks?due_window=overdue")
    assert overdue.status_code == 200
    overdue_tasks = overdue.get_json()
    assert len(overdue_tasks) == 1
    assert overdue_tasks[0]["title"] == "Low overdue"

    by_priority = client.get("/tasks?priority=high")
    assert by_priority.status_code == 200
    priority_tasks = by_priority.get_json()
    assert len(priority_tasks) == 1
    assert priority_tasks[0]["title"] == "High urgent"

    by_tag = client.get("/tasks?tag=home")
    assert by_tag.status_code == 200
    tag_tasks = by_tag.get_json()
    assert len(tag_tasks) == 1
    assert tag_tasks[0]["title"] == "Medium today"

    sorted_priority = client.get("/tasks?sort_by=priority&order=asc")
    assert sorted_priority.status_code == 200
    sorted_tasks = sorted_priority.get_json()
    assert sorted_tasks[0]["priority"] == "high"
