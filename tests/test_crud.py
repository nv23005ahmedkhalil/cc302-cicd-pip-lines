import sys
import os
import pytest

# Ensure app module can be imported when running tests from repo root
sys.path.insert(0, os.path.abspath("app"))

from app import app as flask_app


@pytest.fixture
def client(tmp_path):
    """Create a test client and isolate the tasks storage to a temp file."""
    flask_app.config["TESTING"] = True
    # Point the app's TASKS_FILE to a temp file so tests don't touch repo data
    tasks_file = tmp_path / "tasks.json"
    flask_app.TASKS_FILE = str(tasks_file)
    # Ensure clean start
    if tasks_file.exists():
        tasks_file.unlink()

    with flask_app.test_client() as client:
        yield client


def test_create_task(client):
    # Arrange / Act: create
    resp = client.post("/tasks", json={"title": "Buy milk"})
    # Assert: created
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["title"] == "Buy milk"

    # Read/Verify: list contains the task
    resp2 = client.get("/tasks")
    assert resp2.status_code == 200
    tasks = resp2.get_json()
    assert any(t["title"] == "Buy milk" for t in tasks)


def test_update_task(client):
    # Arrange: create a task first
    create = client.post("/tasks", json={"title": "Old title"})
    assert create.status_code == 201
    task_id = create.get_json()["id"]

    # Act: update
    update = client.put(f"/tasks/{task_id}", json={"title": "New title"})
    assert update.status_code == 200

    # Assert / Read: list contains updated title
    resp2 = client.get("/tasks")
    tasks = resp2.get_json()
    assert any(t["title"] == "New title" for t in tasks)


def test_delete_task(client):
    # Arrange: create
    create = client.post("/tasks", json={"title": "To be deleted"})
    assert create.status_code == 201
    task_id = create.get_json()["id"]

    # Act: delete
    delete = client.delete(f"/tasks/{task_id}")
    assert delete.status_code == 200

    # Assert / Read: task no longer in list
    resp2 = client.get("/tasks")
    tasks = resp2.get_json()
    assert all(t["id"] != task_id for t in tasks)


# NOTE: For the assignment you must produce one intentional failure (run pytest
# with a modified assertion to capture a failing screenshot), then revert the
# change to get back to green. Take a screenshot named `tests-failure.png` for
# the failing run and `tests-passing.png` for the green run.
