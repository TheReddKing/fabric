from enum import Enum

class GlobalC(Enum):
    RELATIONAL_EMBEDDER = 1


class Globals:
    _dict = {}
    def __init__(self):
        if GlobalC.RELATIONAL_EMBEDDER not in Globals._dict:
            Globals._dict[GlobalC.RELATIONAL_EMBEDDER] = {"replaceSpace":'1'}
            # print("NEW")
    @property
    def dict(self):
        return type(self)._dict

    @staticmethod
    def get(key,ans):
        return Globals._dict[key][ans]
    @staticmethod
    def set(key,ans,val):
        Globals._dict[key][ans] = val
        # print(key,ans,Globals._dict[key][ans])
global_settings = Globals()
