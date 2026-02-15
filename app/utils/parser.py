"""
Smart Natural Language Parser for Task Quick-Add
Parses one-line input like: "Submit report tomorrow 6pm !high #school"
Extracts: title, priority, tags, due_date, time
"""
import re
from datetime import datetime, timedelta


def parse_quick_add(text):
    """
    Parse natural language input into task components.
    
    Args:
        text (str): Input text like "Submit report tomorrow 6pm !high #school"
    
    Returns:
        dict: {
            'title': str,
            'priority': str ('low', 'medium', 'high'),
            'tags': list,
            'due_date': str (YYYY-MM-DD),
            'time': str (HH:MM),
            'parse_metadata': {
                'success': bool,
                'warnings': list,
                'original': str
            }
        }
    """
    original_text = text
    warnings = []
    success = True
    
    result = {
        'title': text.strip(),
        'priority': 'medium',
        'tags': [],
        'due_date': datetime.now().strftime('%Y-%m-%d'),
        'time': '09:00',
        'parse_metadata': {
            'success': True,
            'warnings': [],
            'original': original_text
        }
    }
    
    # Extract priority: !high, !medium, !low
    priority_match = re.search(r'!(high|medium|low)', text, re.IGNORECASE)
    if priority_match:
        result['priority'] = priority_match.group(1).lower()
        text = re.sub(r'!(high|medium|low)', '', text, flags=re.IGNORECASE)
    else:
        # Legacy support: !!!, !!, !
        if '!!!' in text or '!!!!' in text:
            result['priority'] = 'high'
            text = re.sub(r'!{3,}', '', text)
        elif '!!' in text:
            result['priority'] = 'high'
            text = re.sub(r'!!', '', text)
        elif '!' in text:
            result['priority'] = 'medium'
            text = re.sub(r'!', '', text)
    
    # Extract tags: #tag1 #tag2
    tags = re.findall(r'#(\w+)', text)
    if tags:
        result['tags'] = tags
        text = re.sub(r'#\w+', '', text)
    
    # Extract time: 6pm, 18:00, at 6pm, at 18:30
    time_parsed = False
    
    # Pattern: HH:MM (24-hour)
    time_match = re.search(r'\b(\d{1,2}):(\d{2})\b', text)
    if time_match:
        hour = int(time_match.group(1))
        minute = time_match.group(2)
        if 0 <= hour <= 23:
            result['time'] = f"{hour:02d}:{minute}"
            text = re.sub(r'\b\d{1,2}:\d{2}\b', '', text)
            time_parsed = True
        else:
            warnings.append(f"Invalid hour: {hour} (must be 0-23)")
    
    # Pattern: 6pm, 12am
    if not time_parsed:
        time_match = re.search(r'\b(\d{1,2})\s*(am|pm)\b', text, re.IGNORECASE)
        if time_match:
            hour = int(time_match.group(1))
            period = time_match.group(2).lower()
            
            if period == 'pm' and hour != 12:
                hour += 12
            elif period == 'am' and hour == 12:
                hour = 0
            
            if 0 <= hour <= 23:
                result['time'] = f"{hour:02d}:00"
                text = re.sub(r'\b\d{1,2}\s*(?:am|pm)\b', '', text, flags=re.IGNORECASE)
                time_parsed = True
            else:
                warnings.append(f"Invalid hour after am/pm conversion: {hour}")
    
    # Extract date: today, tomorrow, next week, Monday, etc.
    date_parsed = False
    today = datetime.now()
    
    # Relative dates
    if re.search(r'\btomorrow\b', text, re.IGNORECASE):
        result['due_date'] = (today + timedelta(days=1)).strftime('%Y-%m-%d')
        text = re.sub(r'\btomorrow\b', '', text, flags=re.IGNORECASE)
        date_parsed = True
    elif re.search(r'\btoday\b', text, re.IGNORECASE):
        result['due_date'] = today.strftime('%Y-%m-%d')
        text = re.sub(r'\btoday\b', '', text, flags=re.IGNORECASE)
        date_parsed = True
    elif re.search(r'\bnext\s+week\b', text, re.IGNORECASE):
        result['due_date'] = (today + timedelta(days=7)).strftime('%Y-%m-%d')
        text = re.sub(r'\bnext\s+week\b', '', text, flags=re.IGNORECASE)
        date_parsed = True
    
    # Weekday names (next Monday, Friday, etc.)
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    for i, day in enumerate(weekdays):
        pattern = rf'\b(?:next\s+)?{day}\b'
        if re.search(pattern, text, re.IGNORECASE):
            days_ahead = i - today.weekday()
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            result['due_date'] = (today + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
            date_parsed = True
            break
    
    # Specific date: MM/DD/YYYY or YYYY-MM-DD
    if not date_parsed:
        date_match = re.search(r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b', text)
        if date_match:
            try:
                month, day, year = int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3))
                parsed_date = datetime(year, month, day)
                result['due_date'] = parsed_date.strftime('%Y-%m-%d')
                text = re.sub(r'\b\d{1,2}/\d{1,2}/\d{4}\b', '', text)
                date_parsed = True
            except ValueError:
                warnings.append(f"Invalid date: {date_match.group(0)}")
    
    # Clean up title
    result['title'] = re.sub(r'\s+', ' ', text).strip()
    
    # Validate title
    if not result['title']:
        warnings.append("No title extracted - using original text")
        result['title'] = original_text.strip()
        success = False
    
    # Update metadata
    result['parse_metadata']['success'] = success
    result['parse_metadata']['warnings'] = warnings
    
    return result


def validate_task_data(data):
    """
    Validate parsed task data before creation.
    
    Returns:
        (bool, str): (is_valid, error_message)
    """
    if not data.get('title'):
        return False, "Title is required"
    
    if len(data['title']) > 200:
        return False, "Title too long (max 200 characters)"
    
    if data.get('priority') not in ['low', 'medium', 'high']:
        return False, "Priority must be 'low', 'medium', or 'high'"
    
    if data.get('tags'):
        if len(data['tags']) > 10:
            return False, "Too many tags (max 10)"
        for tag in data['tags']:
            if len(tag) > 20:
                return False, f"Tag '{tag}' too long (max 20 characters)"
    
    return True, None
