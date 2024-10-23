from aiogram.filters import BaseFilter
from aiogram.types import Message

class isCells(BaseFilter):
    def __init__(self) -> None:
        self.cells = data = {"ᅠ"*i for i in range(1, 10)}
    
    async def __call__(self, message: Message) -> bool:
        return message.text in self.cells
