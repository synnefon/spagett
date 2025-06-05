data_sources = {
    "users": [
        {"id": 1, "name": "Alice", "age": 28, "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "age": 35, "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "age": 22, "email": "charlie@example.com"},
        {"id": 4, "name": "Dorothy", "age": 88, "email": "dorothy@example.com"},
    ],
    "roleplays": [
        {"oid": 100, "user_id": 1, "completed": True, "duration_seconds": 100},
        {"oid": 101, "user_id": 2, "completed": False, "duration_seconds": 200},
        {"oid": 102, "user_id": 1, "completed": False, "duration_seconds": 300},
        {"oid": 103, "user_id": 4, "completed": True, "duration_seconds": 100},
        {"oid": 104, "user_id": 4, "completed": True, "duration_seconds": 200},
        {"oid": 105, "user_id": 3, "completed": False, "duration_seconds": 200},
    ],
    "evaluations": [
        {"eid": 200, "roleplay_id": 100, "performance": 3},
        {"eid": 201, "roleplay_id": 101, "performance": 9},
        {"eid": 202, "roleplay_id": 102, "performance": 4},
        {"eid": 203, "roleplay_id": 103, "performance": 10},
        {"eid": 204, "roleplay_id": 104, "performance": 5},
        {"eid": 205, "roleplay_id": 105, "performance": 6},
        {"eid": 206, "roleplay_id": 105, "performance": 7},
        {"eid": 207, "roleplay_id": 105, "performance": 1},
    ]
}
