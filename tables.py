data_sources = {
    "users": [
        {"id": 1, "name": "Alice", "age": 28, "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "age": 35, "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "age": 22, "email": "charlie@example.com"},
        {"id": 4, "name": "Andrew", "age": 88, "email": "andrew@example.com"},
    ],
    "roleplays": [
        {"id": 100, "user_id": 1, "completed": True, "duration_seconds": 100},
        {"id": 101, "user_id": 2, "completed": False, "duration_seconds": 200},
        {"id": 102, "user_id": 1, "completed": False, "duration_seconds": 300},
        {"id": 103, "user_id": 4, "completed": True, "duration_seconds": 100},
        {"id": 104, "user_id": 4, "completed": True, "duration_seconds": 200},
        {"id": 105, "user_id": 3, "completed": False, "duration_seconds": 200},
    ],
}
