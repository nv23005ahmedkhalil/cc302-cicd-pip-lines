"""
Focus Session Manager
Handles task focus timers, session tracking, and aggregations.
"""
import json
import os
from datetime import datetime


FOCUS_SESSIONS_FILE = "focus_sessions.json"
ACTIVE_SESSIONS_FILE = "active_sessions.json"


def load_focus_sessions():
    """Load historical focus sessions"""
    if os.path.exists(FOCUS_SESSIONS_FILE):
        with open(FOCUS_SESSIONS_FILE, "r") as f:
            return json.load(f)
    return []


def save_focus_sessions(sessions):
    """Save focus sessions history"""
    with open(FOCUS_SESSIONS_FILE, "w") as f:
        json.dump(sessions, f, indent=4)


def load_active_sessions():
    """Load currently active focus sessions"""
    if os.path.exists(ACTIVE_SESSIONS_FILE):
        with open(ACTIVE_SESSIONS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_active_sessions(sessions):
    """Save active sessions"""
    with open(ACTIVE_SESSIONS_FILE, "w") as f:
        json.dump(sessions, f, indent=4)


def start_focus_session(task_id, duration_preset=25):
    """
    Start a focus session for a task.
    
    Args:
        task_id (int): Task ID
        duration_preset (int): Suggested duration in minutes (25 or 50)
    
    Returns:
        dict: Session info or error
    """
    active_sessions = load_active_sessions()
    
    # Check if task already has active session
    task_key = str(task_id)
    if task_key in active_sessions:
        return {
            "error": "Task already has an active focus session",
            "session": active_sessions[task_key]
        }, False
    
    # Create new session
    session = {
        "task_id": task_id,
        "started_at": datetime.now().isoformat(),
        "duration_preset": duration_preset,
        "status": "active"
    }
    
    active_sessions[task_key] = session
    save_active_sessions(active_sessions)
    
    return session, True


def stop_focus_session(task_id):
    """
    Stop a focus session and calculate duration.
    
    Returns:
        (dict, int, dict): (session_data, focus_minutes, suggestions)
    """
    active_sessions = load_active_sessions()
    task_key = str(task_id)
    
    if task_key not in active_sessions:
        return None, 0, {"error": "No active session found for this task"}
    
    session = active_sessions[task_key]
    session["ended_at"] = datetime.now().isoformat()
    session["status"] = "completed"
    
    # Calculate duration
    start_time = datetime.fromisoformat(session["started_at"])
    end_time = datetime.fromisoformat(session["ended_at"])
    duration = (end_time - start_time).total_seconds() / 60  # minutes
    session["actual_duration"] = round(duration, 2)
    
    # Save to history
    history = load_focus_sessions()
    history.append(session)
    save_focus_sessions(history)
    
    # Remove from active
    del active_sessions[task_key]
    save_active_sessions(active_sessions)
    
    # Generate suggestions
    suggestions = generate_suggestions(duration, session["duration_preset"])
    
    return session, int(duration), suggestions


def generate_suggestions(actual_minutes, preset_minutes):
    """
    Generate status change suggestions based on focus time.
    
    Returns:
        dict: Suggestions for user
    """
    suggestions = {
        "status_change": None,
        "message": "",
        "achievement": None
    }
    
    # Suggest status changes
    if actual_minutes >= preset_minutes * 0.9:  # Completed 90%+ of preset
        suggestions["status_change"] = "done"
        suggestions["message"] = "Great focus session! Consider marking this task as done."
        suggestions["achievement"] = "Full session completed!"
    elif actual_minutes >= preset_minutes * 0.5:  # Completed 50%+
        suggestions["status_change"] = "doing"
        suggestions["message"] = "Good progress! Task moved to 'doing' status."
    else:
        suggestions["message"] = f"Short session ({int(actual_minutes)} min). Keep going!"
    
    # Achievement badges
    if actual_minutes >= 50:
        suggestions["achievement"] = "Deep Work Master 🎯"
    elif actual_minutes >= 25:
        suggestions["achievement"] = "Pomodoro Champion 🍅"
    
    return suggestions


def get_today_stats(task_id=None):
    """
    Get focus statistics for today.
    
    Args:
        task_id (int, optional): If provided, get stats for specific task
    
    Returns:
        dict: Stats including total_minutes, session_count, etc.
    """
    sessions = load_focus_sessions()
    today = datetime.now().date().isoformat()
    
    today_sessions = [
        s for s in sessions
        if s.get("ended_at", "").startswith(today)
    ]
    
    if task_id:
        today_sessions = [s for s in today_sessions if s["task_id"] == task_id]
    
    total_minutes = sum(s.get("actual_duration", 0) for s in today_sessions)
    
    return {
        "today": today,
        "total_focus_minutes": round(total_minutes, 2),
        "session_count": len(today_sessions),
        "sessions": today_sessions,
        "task_id": task_id
    }


def get_active_session_status(task_id):
    """
    Check if task has an active focus session.
    
    Returns:
        dict or None: Active session info if exists
    """
    active_sessions = load_active_sessions()
    task_key = str(task_id)
    
    if task_key in active_sessions:
        session = active_sessions[task_key]
        # Calculate elapsed time
        start_time = datetime.fromisoformat(session["started_at"])
        elapsed = (datetime.now() - start_time).total_seconds() / 60
        session["elapsed_minutes"] = round(elapsed, 2)
        return session
    
    return None
