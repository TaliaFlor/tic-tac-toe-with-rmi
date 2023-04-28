from typing import TypedDict


class Player(TypedDict):
    id: int
    symbol: str
    active: bool
    color: tuple[int, int, int]
