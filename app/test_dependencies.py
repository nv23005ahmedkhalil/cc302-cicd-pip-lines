#!/usr/bin/env python3
"""
Test Task Dependencies Feature
Tests dependency validation, circular detection, and blocked task logic
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    print(f"Response:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)


def test_task_dependencies():
    """Run complete task dependency test suite"""
    
    print("\n🔹 Step 1: Create test tasks (A → B → C chain)")
    
    # Task A (depends on nothing)
    task_a = requests.post(
        f"{BASE_URL}/tasks",
        json={"title": "Task A - Foundation", "priority": "high"}
    )
    print_response("Create Task A", task_a)
    task_a_id = task_a.json()['id']
    
    # Task B (will depend on A)
    task_b = requests.post(
        f"{BASE_URL}/tasks",
        json={"title": "Task B - Build on A", "priority": "medium"}
    )
    print_response("Create Task B", task_b)
    task_b_id = task_b.json()['id']
    
    # Task C (will depend on B)
    task_c = requests.post(
        f"{BASE_URL}/tasks",
        json={"title": "Task C - Final step", "priority": "low"}
    )
    print_response("Create Task C", task_c)
    task_c_id = task_c.json()['id']
    
    # ===== Test Dependency Addition =====
    
    print(f"\n🔹 Step 2: Make B depend on A (B → A)")
    dep1 = requests.post(
        f"{BASE_URL}/tasks/{task_b_id}/dependencies",
        json={"dependency_id": task_a_id}
    )
    print_response(f"Add Dependency: B→A", dep1)
    
    print(f"\n🔹 Step 3: Make C depend on B (C → B)")
    dep2 = requests.post(
        f"{BASE_URL}/tasks/{task_c_id}/dependencies",
        json={"dependency_id": task_b_id}
    )
    print_response(f"Add Dependency: C→B", dep2)
    
    # ===== Test Circular Dependency Detection =====
    
    print(f"\n🔹 Step 4: Try to create circular dependency (A → C)")
    print("   This would create: A → C → B → A (circular!)")
    circular = requests.post(
        f"{BASE_URL}/tasks/{task_a_id}/dependencies",
        json={"dependency_id": task_c_id}
    )
    print_response("Circular Dependency Test (Should Fail)", circular)
    
    # ===== Test Self-Dependency =====
    
    print(f"\n🔹 Step 5: Try to make task depend on itself")
    self_dep = requests.post(
        f"{BASE_URL}/tasks/{task_a_id}/dependencies",
        json={"dependency_id": task_a_id}
    )
    print_response("Self-Dependency Test (Should Fail)", self_dep)
    
    # ===== Test Dependency Chain =====
    
    print(f"\n🔹 Step 6: Get full dependency chain for Task C")
    chain = requests.get(f"{BASE_URL}/tasks/{task_c_id}/dependency-chain")
    print_response("Dependency Chain (C→B→A)", chain)
    
    # ===== Test Blocked Status =====
    
    print(f"\n🔹 Step 7: Check if Task C is blocked")
    blocked = requests.get(f"{BASE_URL}/tasks/{task_c_id}/blocked")
    print_response("Check Blocked Status", blocked)
    
    # ===== Test Blocked Completion =====
    
    print(f"\n🔹 Step 8: Try to complete Task C (should fail - blocked)")
    complete_c = requests.put(
        f"{BASE_URL}/tasks/{task_c_id}",
        json={"completed": True}
    )
    print_response("Complete Blocked Task (Should Fail)", complete_c)
    
    # ===== Test Valid Completion Sequence =====
    
    print(f"\n🔹 Step 9: Complete Task A (no dependencies)")
    complete_a = requests.put(
        f"{BASE_URL}/tasks/{task_a_id}",
        json={"completed": True}
    )
    print_response("Complete Task A (Should Succeed)", complete_a)
    
    print(f"\n🔹 Step 10: Check if Task B is still blocked")
    blocked_b = requests.get(f"{BASE_URL}/tasks/{task_b_id}/blocked")
    print_response("Check B Blocked Status (Should be Unblocked)", blocked_b)
    
    print(f"\n🔹 Step 11: Complete Task B")
    complete_b = requests.put(
        f"{BASE_URL}/tasks/{task_b_id}",
        json={"completed": True}
    )
    print_response("Complete Task B (Should Succeed)", complete_b)
    
    print(f"\n🔹 Step 12: Now complete Task C (should succeed)")
    complete_c2 = requests.put(
        f"{BASE_URL}/tasks/{task_c_id}",
        json={"completed": True}
    )
    print_response("Complete Task C (Should Succeed Now)", complete_c2)
    
    # ===== Test Dependency Removal =====
    
    print(f"\n🔹 Step 13: Create new task D")
    task_d = requests.post(
        f"{BASE_URL}/tasks",
        json={"title": "Task D - Test removal"}
    )
    task_d_id = task_d.json()['id']
    
    print(f"\n🔹 Step 14: Add dependency D→A")
    dep_d = requests.post(
        f"{BASE_URL}/tasks/{task_d_id}/dependencies",
        json={"dependency_id": task_a_id}
    )
    print_response("Add Dependency D→A", dep_d)
    
    print(f"\n🔹 Step 15: Remove dependency D→A")
    remove_dep = requests.delete(
        f"{BASE_URL}/tasks/{task_d_id}/dependencies/{task_a_id}"
    )
    print_response("Remove Dependency", remove_dep)
    
    print(f"\n🔹 Step 16: Verify D has no dependencies")
    blocked_d = requests.get(f"{BASE_URL}/tasks/{task_d_id}/blocked")
    print_response("Check D Blocked (Should be Unblocked)", blocked_d)
    
    print("\n✅ All dependency tests completed!\n")


if __name__ == "__main__":
    print("=" * 60)
    print("  TASK DEPENDENCIES TEST SUITE")
    print("=" * 60)
    print("\n⚠️  Make sure the Flask app is running on http://localhost:5000")
    print("    Run: python3 app.py\n")
    
    try:
        requests.get(BASE_URL, timeout=2)
        test_task_dependencies()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to Flask app.")
        print("   Start the app first: python3 app.py")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
