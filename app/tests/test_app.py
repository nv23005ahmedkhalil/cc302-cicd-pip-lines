"""
Basic integration tests for Flask Todo App.
Tests that the app can be imported and responds to requests.
"""
import pytest
import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_app_import():
    """Test that the app can be imported."""
    from app import app
    assert app is not None
    assert app.config


def test_app_responds_to_root():
    """Smoke test: app responds to root route."""
    from app import app
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        response = client.get('/')
        # Expect either 200 (HTML) or 302 (redirect)
        assert response.status_code in [200, 302], f"Got {response.status_code}"


def test_app_get_tasks_endpoint():
    """Smoke test: /tasks endpoint exists and returns JSON."""
    from app import app
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        response = client.get('/tasks')
        # Should return 200 OK
        assert response.status_code == 200
        # Should return JSON list
        assert isinstance(response.get_json(), list)


def test_app_post_task():
    """Test: Can create a task via POST."""
    from app import app
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        response = client.post(
            '/tasks',
            json={'title': 'Test Task', 'description': 'A test task'}
        )
        assert response.status_code in [200, 201]
        data = response.get_json()
        assert data['title'] == 'Test Task'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
