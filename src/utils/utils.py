import random
from collections import deque


def check_winners(playground: list[int], player: int) -> bool:
    n = len(playground)
    if playground[0] == playground[4] == playground[8] and playground[0] == player:
        return True
    elif playground[6] == playground[4] == playground[2] and playground[2] == player:
        return True

    for i in range(n//3):
        if playground[i] == playground[i+3] == playground[i+6] and playground[i] == player:
            return True
        if playground[3*i] == playground[3*i+1] == playground[3*i+2] and playground[3*i] == player:
            return True
    
    return False


def make_next_move(playground: list[int], level: int=0) -> int:
    '''
    следуйщий ход для бота
    '''
    # TODO: сделать сложную версию (3 уровня сложности )
    rnd = random.randint(0, 8)
    while playground[rnd] != 0:
        rnd = random.randint(0, 8)
    
    return rnd


def is_full(playground: list[int]) -> bool:
    '''
        Проверка если свободная клетка для хода
    '''
    return playground.count(0) == 0


def move_position(pos: int, is_human: bool) -> str:
    if is_human:
        return f"Ваш ход, строка {pos//3+1}, стольбец {pos%3+1}: " 
    
    return f"Мой ход, строка {pos//3+1}, стольбец {pos%3+1}: "



def get_random_number(start: int, end: int) -> int:
    return random.randint(start, end)

# def process_new_pg(stack: list[int]) -> list:
#     new_pg = [0] * 9
#     for ind, pos in enumerate(stack):
#         if ind%2 == 0:
#             new_pg[pos] = 1
#         else: 
#             new_pg[pos] = 2
#     return new_pg[:]


def process_make_new_game(user: dict[str, any]) -> None:
    user["pg"] = [0 for _ in range(9)]
    user["stack"] = deque()
    user["reStack"] = deque()


def procces_first_bot_move(users: dict, user_id: int):
    pos = make_next_move(users[user_id]["pg"])
    users[user_id]["stack"].append(pos)
    users[user_id]["pg"][pos] = 2

