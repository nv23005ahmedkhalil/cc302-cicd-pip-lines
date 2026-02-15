from utils.parser import parse_quick_add
import json

# Test cases
test_inputs = [
    "Submit report tomorrow 6pm !high #school #work",
    "Buy groceries today 2pm !low #personal",
    "Team meeting next monday 10:00 !medium #work",
    "Call mom friday 7pm #family",
    "No metadata task"
]

for text in test_inputs:
    print(f"\nInput: {text}")
    result = parse_quick_add(text)
    print(json.dumps(result, indent=2))
    print("-" * 60)
