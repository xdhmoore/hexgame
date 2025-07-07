
from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Self
from venv import logging
from blessed.keyboard import Keystroke



class StateType(StrEnum):
    PICK_PIECE = ("PICK_PIECE")
    PLACE_PIECE = ("PLACE_PIECE")

    def __init__(self, type):
        self.type = type


class AbstractState(ABC):
    _instance = None

    # Singleton
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @abstractmethod
    def on_key(self, ks, mgr) -> tuple[Self | None, bool]:
        pass

    @abstractmethod
    def gs_type(self) -> StateType:
        pass

    def on_key_shared(self, ks: Keystroke, mgr, next_state, actions_taken) -> tuple[Self | None, bool]:

        if ks == 'w' or ks == 'W':
            logging.debug("W")
            mgr.view_offset = (
                mgr.view_offset[0] - 1,
                mgr.view_offset[1]
            )
            actions_taken = True

        if ks == 's' or ks == 'S':
            logging.debug("S")
            mgr.view_offset = (
                mgr.view_offset[0] + 1,
                mgr.view_offset[1]
            )
            actions_taken = True

        if ks == 'a' or ks == 'A':
            logging.debug("A")
            mgr.view_offset = (
                mgr.view_offset[0],
                mgr.view_offset[1] - 1,
            )
            actions_taken = True

        if ks == 'd' or ks == 'D':
            logging.debug("D")
            mgr.view_offset = (
                mgr.view_offset[0],
                mgr.view_offset[1] + 1,
            )
            actions_taken = True

        return (next_state, actions_taken)

