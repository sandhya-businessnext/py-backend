from typing import Any

name:str = 'Sandhya'

age:int = 27

members:tuple[str,...]  = ('Mom','Sammu', 'Di','Shivam', name)

assets:list[int|str] = [1,'san',2,3,'ab']

collect:dict[str,Any] = {
    "name":name,
    "age":age
}

def pow(base:int, exp:int | None) -> float:
    
    return pow(base, 2 if exp is None else exp)