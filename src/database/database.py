from collections import deque

TEMPLATE_USER = {
    "isBot": False,
    "level": 1,
    "pg": [0 for _ in range(9)],
    "stack": deque(),
    "rStack": deque(),
}

# создаем странную базуданных
users = {
}