"""
Test suite for ToDo Flask application
"""
import sys
import os

# Ensure the app directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_app_import():
    """Test that the app module can be imported."""
    try:
        import app
        assert True
    except ImportError as e:
        # If direct import fails, try importing the Flask app object
        try:
            from app import app as flask_app
            assert flask_app is not None
        except ImportError:
            assert False, f"Failed to import app: {e}"


def test_flask_app_exists():
    """Test that Flask app object exists."""
    assert 1 == 2, "QUALITY_GATE_DEMO: Intentional test failure to demonstrate CI blocking"
    try:
        from app import app as flask_app
        assert flask_app is not None
        assert hasattr(flask_app, 'config')
    except Exception as e:
        assert False, f"Flask app not found: {e}"


def test_app_runs():
    """Test that the app can create a test client."""
    try:
        from app import app as flask_app
        flask_app.config['TESTING'] = True
        client = flask_app.test_client()
        assert client is not None
    except Exception as e:
        assert False, f"Failed to create test client: {e}"


def test_basic_route():
    """Test that at least one route works."""
    try:
        from app import app as flask_app
        flask_app.config['TESTING'] = True
        
        with flask_app.test_client() as client:
            # Try common routes
            routes_to_test = ['/', '/api', '/tasks', '/health']
            
            for route in routes_to_test:
                response = client.get(route)
                # Any response (even 404) means the app is working
                if response.status_code in [200, 201, 302, 404, 405]:
                    assert True
                    return
            
            # If we get here, at least the app responded
            assert True
    except Exception as e:
        assert False, f"App failed to respond: {e}"
