import json


def add_todo():
    todos = get_todos()
    todo_id = max((int(k) for k in todos.keys()), default=0) + 1
    content = input("Enter todo content \n")
    todos[str(todo_id)] = {"id":todo_id, "content":content}
    with open("todos.json","w") as f:
        json.dump(todos,f,indent=4)
    
def get_todos():
    try:
        with open("todos.json","r") as f:
            todos = json.load(f)
            return todos
    except(FileNotFoundError, json.JSONDecodeError):
        return {}



add_todo()