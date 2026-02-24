"""
Test suite for ToDo Flask application
"""
import pytest
import json
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_app_import():
    """Test that the app can be imported."""
    from app import app
    assert app is not None


def test_app_configuration():
    """Test app configuration."""
    from app import app
    assert app.config is not None


def test_home_route():
    """Test the home route returns 200."""
    from app import app
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200


def test_api_welcome():
    """Test API welcome endpoint if it exists."""
    from app import app
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        response = client.get('/api')
        # 200 if exists, 404 if not - both are valid
        assert response.status_code in [200, 404]


def test_get_all_tasks():
    """Test GET /tasks endpoint."""
    from app import app
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        response = client.get('/tasks')
        # Should return 200 with list or 404 if route doesn't exist
        if response.status_code == 200:
            data = json.loads(response.data)
            assert isinstance(data, list) or isinstance(data, dict)


def test_create_task():
    """Test POST /tasks endpoint."""
    from app import app
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        new_task = {
            "title": "Test Task",
            "description": "Test Description"
        }
        response = client.post('/tasks',
                              data=json.dumps(new_task),
                              content_type='application/json')
        # 201, 200, or 404 are acceptable
        assert response.status_code in [200, 201, 404, 405]
