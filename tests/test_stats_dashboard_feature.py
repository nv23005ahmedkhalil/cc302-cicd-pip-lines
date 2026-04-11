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


def test_task_stats_dashboard(client):
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    completed_task = client.post(
        "/tasks",
        json={"title": "Completed", "date": yesterday, "priority": "high"},
    )
    assert completed_task.status_code == 201
    completed_id = completed_task.get_json()["id"]

    mark_complete = client.put(f"/tasks/{completed_id}", json={"completed": True})
    assert mark_complete.status_code == 200

    overdue_task = client.post(
        "/tasks",
        json={"title": "Overdue", "date": yesterday, "priority": "medium"},
    )
    assert overdue_task.status_code == 201

    today_task = client.post(
        "/tasks",
        json={"title": "Today", "date": today, "priority": "low"},
    )
    assert today_task.status_code == 201

    stats = client.get("/api/tasks/stats")
    assert stats.status_code == 200

    payload = stats.get_json()
    assert payload["total_tasks"] == 3
    assert payload["completed_tasks"] == 1
    assert payload["overdue_tasks"] == 1
    assert len(payload["completion_trend_last_7_days"]) == 7
