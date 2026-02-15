"""
Task Dependency Manager
Handles task dependencies, circular detection, and blocking logic.
"""


def detect_circular_dependency(task_id, new_dependency_id, tasks):
    """
    Detect if adding new_dependency_id as a dependency of task_id
    would create a circular dependency.
    
    Uses DFS to check if there's a path from new_dependency_id back to task_id.
    
    Args:
        task_id (int): The task that will depend on new_dependency_id
        new_dependency_id (int): The proposed dependency
        tasks (list): All tasks
    
    Returns:
        (bool, list): (has_circular, cycle_path)
    """
    # Build dependency graph
    dep_graph = {}
    for task in tasks:
        tid = task['id']
        deps = task.get('depends_on', [])
        dep_graph[tid] = deps.copy()
    
    # Simulate adding the new dependency
    if task_id not in dep_graph:
        dep_graph[task_id] = []
    dep_graph[task_id].append(new_dependency_id)
    
    # DFS to detect cycle
    visited = set()
    rec_stack = set()
    path = []
    
    def dfs(node, target, current_path):
        """Depth-first search to find path from node to target"""
        if node in rec_stack:
            # Found a cycle
            return True, current_path + [node]
        
        if node in visited:
            return False, []
        
        visited.add(node)
        rec_stack.add(node)
        current_path.append(node)
        
        # Check all dependencies of this node
        for dep in dep_graph.get(node, []):
            if dep == target:
                # Found path back to target - circular!
                return True, current_path + [dep]
            
            has_cycle, cycle_path = dfs(dep, target, current_path.copy())
            if has_cycle:
                return True, cycle_path
        
        rec_stack.remove(node)
        return False, []
    
    # Check if there's a path from new_dependency back to task_id
    has_cycle, cycle = dfs(new_dependency_id, task_id, [])
    
    return has_cycle, cycle


def get_blocking_tasks(task, tasks):
    """
    Get list of tasks that are blocking this task.
    
    Args:
        task (dict): The task to check
        tasks (list): All tasks
    
    Returns:
        list: List of blocking task objects (dependencies that aren't done)
    """
    depends_on = task.get('depends_on', [])
    if not depends_on:
        return []
    
    blocking = []
    for dep_id in depends_on:
        dep_task = next((t for t in tasks if t['id'] == dep_id), None)
        if dep_task and not dep_task.get('completed', False):
            blocking.append(dep_task)
    
    return blocking


def is_blocked(task, tasks):
    """
    Check if task is blocked by incomplete dependencies.
    
    Returns:
        (bool, list): (is_blocked, blocking_tasks)
    """
    blocking_tasks = get_blocking_tasks(task, tasks)
    return len(blocking_tasks) > 0, blocking_tasks


def validate_dependencies(task_id, dependency_ids, tasks):
    """
    Validate a list of dependencies for a task.
    
    Returns:
        (bool, str, list): (is_valid, error_message, circular_path)
    """
    # Check all dependencies exist
    existing_ids = {t['id'] for t in tasks}
    
    for dep_id in dependency_ids:
        if dep_id not in existing_ids:
            return False, f"Dependency task #{dep_id} does not exist", []
        
        if dep_id == task_id:
            return False, "Task cannot depend on itself", [task_id, task_id]
    
    # Check for circular dependencies
    temp_tasks = tasks.copy()
    task_idx = next((i for i, t in enumerate(temp_tasks) if t['id'] == task_id), None)
    
    for dep_id in dependency_ids:
        has_circular, cycle = detect_circular_dependency(task_id, dep_id, temp_tasks)
        if has_circular:
            return False, f"Circular dependency detected: {' -> '.join(map(str, cycle))}", cycle
    
    return True, None, []


def add_dependency(task_id, dependency_id, tasks):
    """
    Add a dependency to a task.
    
    Returns:
        (bool, str, dict): (success, message, updated_task)
    """
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return False, "Task not found", None
    
    # Initialize depends_on if not exists
    if 'depends_on' not in task:
        task['depends_on'] = []
    
    # Check if already depends
    if dependency_id in task['depends_on']:
        return False, f"Task already depends on #{dependency_id}", task
    
    # Validate
    is_valid, error, cycle = validate_dependencies(
        task_id,
        task['depends_on'] + [dependency_id],
        tasks
    )
    
    if not is_valid:
        return False, error, task
    
    # Add dependency
    task['depends_on'].append(dependency_id)
    
    return True, f"Dependency #{dependency_id} added", task


def remove_dependency(task_id, dependency_id, tasks):
    """
    Remove a dependency from a task.
    
    Returns:
        (bool, str, dict): (success, message, updated_task)
    """
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return False, "Task not found", None
    
    depends_on = task.get('depends_on', [])
    
    if dependency_id not in depends_on:
        return False, f"Task does not depend on #{dependency_id}", task
    
    task['depends_on'].remove(dependency_id)
    
    return True, f"Dependency #{dependency_id} removed", task


def get_dependency_chain(task_id, tasks, visited=None):
    """
    Get the full dependency chain for a task (recursive).
    
    Returns:
        list: Ordered list of task IDs that must be completed first
    """
    if visited is None:
        visited = set()
    
    if task_id in visited:
        return []
    
    visited.add(task_id)
    
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return []
    
    chain = []
    depends_on = task.get('depends_on', [])
    
    for dep_id in depends_on:
        # Recursively get dependencies of dependencies
        sub_chain = get_dependency_chain(dep_id, tasks, visited)
        chain.extend(sub_chain)
        chain.append(dep_id)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_chain = []
    for tid in chain:
        if tid not in seen:
            seen.add(tid)
            unique_chain.append(tid)
    
    return unique_chain
