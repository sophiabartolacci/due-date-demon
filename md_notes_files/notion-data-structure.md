# Notion API Data Structure Reference

## Database Query Response Structure

### Top Level - `assignments`
```python
assignments = {
    "object": "list",                    # Type indicator
    "results": [...],                    # List of database entries
    "has_more": False,                   # Pagination indicator
    "next_cursor": None                  # Pagination cursor
}
```

### Results Level - `assignments["results"]`
```python
results = [                              # List of assignment objects
    {                                    # Individual assignment (dict)
        "id": "page_id_string",
        "object": "page", 
        "properties": {...}              # Assignment data
    },
    {                                    # Another assignment
        "id": "another_page_id",
        "properties": {...}
    }
]
```

### Assignment Level - `assignment` (from loop)
```python
assignment = {
    "id": "abc123-def456",
    "object": "page",
    "properties": {                      # Dict of all property data
        "Assignment": {...},             # Title property
        "Class": {...},                  # Select property  
        "Due Date": {...},               # Date property
        "Type": {...},                   # Select property
        "To Do": {...},                  # Checkbox property
        "Notes": {...}                   # Rich text property
    }
}
```

### Property Structures

#### Title Property - `assignment["properties"]["Assignment"]`
```python
"Assignment": {
    "type": "title",
    "title": [                           # List of text blocks
        {
            "plain_text": "Math Homework",
            "text": {"content": "Math Homework"}
        }
    ]
}
```

#### Select Property - `assignment["properties"]["Class"]`
```python
"Class": {
    "type": "select",
    "select": {                          # Dict with selected option
        "id": "option_id",
        "name": "CS 380",
        "color": "purple"
    }
}
```

#### Date Property - `assignment["properties"]["Due Date"]`
```python
"Due Date": {
    "type": "date",
    "date": {                            # Dict with date info
        "start": "2025-08-24",
        "end": null,
        "time_zone": null
    }
}
```

#### Checkbox Property - `assignment["properties"]["To Do"]`
```python
"To Do": {
    "type": "checkbox",
    "checkbox": True                     # Boolean value
}
```

#### Rich Text Property - `assignment["properties"]["Notes"]`
```python
"Notes": {
    "type": "rich_text",
    "rich_text": [                       # List of text blocks
        {
            "plain_text": "Remember to study chapter 5",
            "text": {"content": "Remember to study chapter 5"}
        }
    ]
}
```

## Access Patterns

### Get Assignment Name
```python
name = assignment["properties"]["Assignment"]["title"][0]["plain_text"]
#      dict        dict         dict      list[0] dict
```

### Get Class Name
```python
class_name = assignment["properties"]["Class"]["select"]["name"]
#            dict        dict     dict     dict
```

### Get Due Date
```python
due_date = assignment["properties"]["Due Date"]["date"]["start"]
#          dict        dict         dict    dict
```

### Get Checkbox Status
```python
is_todo = assignment["properties"]["To Do"]["checkbox"]
#         dict        dict         dict
```

## Key Points
- `results` = **list** of assignments
- `assignment` = **dict** for individual assignment
- `properties` = **dict** of all assignment data
- **Title/Rich Text** = lists (need `[0]`)
- **Select/Date/Checkbox** = dicts (direct access)