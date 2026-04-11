import os
import sys

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


def test_search_by_title_and_description(client):
    client.post(
        "/tasks",
        json={"title": "Write design doc", "description": "Architecture notes"},
    )
    client.post(
        "/tasks",
        json={"title": "Buy groceries", "description": "Milk and fruit"},
    )

    by_title = client.get("/tasks?q=design")
    assert by_title.status_code == 200
    title_results = by_title.get_json()
    assert len(title_results) == 1
    assert title_results[0]["title"] == "Write design doc"

    by_description = client.get("/tasks?q=milk")
    assert by_description.status_code == 200
    description_results = by_description.get_json()
    assert len(description_results) == 1
    assert description_results[0]["title"] == "Buy groceries"
