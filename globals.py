from enum import Enum

class GlobalC(Enum):
    RELATIONAL_EMBEDDER = 1


class Globals:
    def __init__(self):
        self.dict = {}
        self.dict[GlobalC.RELATIONAL_EMBEDDER] = {"replaceSpace":True}
    @staticmethod
    def get(key,ans):
        global global_settings
        return global_settings.dict[key][ans]
    @staticmethod
    def set(key,ans,val):
        global global_settings
        global_settings.dict[key][ans] = val

global_settings = Globals()
