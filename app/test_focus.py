#!/usr/bin/env python3
"""
Test Focus Sessions Feature
Tests start/stop timer, duration calculation, and suggestions
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))


def test_focus_sessions():
    """Run complete focus session test suite"""
    
    # 1. Create a test task
    print("\n🔹 Step 1: Create test task")
    task_response = requests.post(
        f"{BASE_URL}/tasks/quick-add",
        json={"text": "Write documentation tomorrow 2pm !high #work"}
    )
    print_response("Create Task via Quick Add", task_response)
    task_id = task_response.json()['id']
    
    # 2. Start focus session (25 min)
    print("\n🔹 Step 2: Start 25-min focus session")
    start_response = requests.post(
        f"{BASE_URL}/tasks/{task_id}/focus/start",
        json={"duration": 25}
    )
    print_response("Start Focus Session", start_response)
    
    # 3. Check active session status
    print("\n🔹 Step 3: Check active session")
    status_response = requests.get(f"{BASE_URL}/tasks/{task_id}/focus/status")
    print_response("Active Session Status", status_response)
    
    # 4. Wait a few seconds to simulate work
    print("\n⏱️  Simulating 3 seconds of focused work...")
    time.sleep(3)
    
    # 5. Stop focus session
    print("\n🔹 Step 4: Stop focus session")
    stop_response = requests.post(f"{BASE_URL}/tasks/{task_id}/focus/stop")
    print_response("Stop Focus Session", stop_response)
    
    # 6. Get today's focus stats
    print("\n🔹 Step 5: Get today's focus statistics")
    stats_response = requests.get(f"{BASE_URL}/api/focus/stats")
    print_response("Today's Focus Stats", stats_response)
    
    # 7. Get task-specific stats
    print(f"\n🔹 Step 6: Get stats for task #{task_id}")
    task_stats_response = requests.get(
        f"{BASE_URL}/api/focus/stats",
        params={"task_id": task_id}
    )
    print_response(f"Task #{task_id} Focus Stats", task_stats_response)
    
    # 8. Try to start another session (test conflict)
    print("\n🔹 Step 7: Start another session immediately")
    start2_response = requests.post(
        f"{BASE_URL}/tasks/{task_id}/focus/start",
        json={"duration": 50}
    )
    print_response("Second Session (Should Work)", start2_response)
    
    # 9. Get final task details
    print(f"\n🔹 Step 8: Get final task details")
    task_details = requests.get(f"{BASE_URL}/tasks/{task_id}")
    print_response("Final Task State", task_details)
    
    print("\n✅ All tests completed!\n")


if __name__ == "__main__":
    print("=" * 60)
    print("  FOCUS SESSIONS TEST SUITE")
    print("=" * 60)
    print("\n⚠️  Make sure the Flask app is running on http://localhost:5000")
    print("    Run: python3 app.py\n")
    
    try:
        requests.get(BASE_URL, timeout=2)
        test_focus_sessions()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to Flask app.")
        print("   Start the app first: python3 app.py")
    except Exception as e:
        print(f"❌ Error: {e}")
