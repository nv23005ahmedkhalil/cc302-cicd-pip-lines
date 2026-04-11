import os
import sys

import pytest

sys.path.insert(0, os.path.abspath("app"))
from app import app as flask_app


@pytest.fixture
def client(tmp_path):
    flask_app.config["TESTING"] = True
    tasks_file = tmp_path / "tasks.json"
    flask_app.TASKS_FILE = str(tasks_file)

    with flask_app.test_client() as client:
        yield client


def test_metadata_fields_and_status_sync(client):
    create = client.post(
        "/tasks",
        json={
            "title": "Metadata task",
            "description": "Need metadata",
            "due_date": "2026-05-01",
            "priority": "high",
            "status": "in_progress",
        },
    )

    assert create.status_code == 201
    task = create.get_json()

    assert task["due_date"] == "2026-05-01"
    assert task["date"] == "2026-05-01"
    assert task["priority"] == "high"
    assert task["status"] == "in_progress"
    assert task["completed"] is False
    assert "updated_at" in task

    update = client.put(f"/tasks/{task['id']}", json={"status": "completed"})
    assert update.status_code == 200
    updated = update.get_json()

    assert updated["status"] == "completed"
    assert updated["completed"] is True
    assert updated["updated_at"] >= task["updated_at"]
