from fastapi import FastAPI, HTTPException, Query, status
from schemas import TodoCreate, TodoUpdate, TodoResponse

app = FastAPI(title="Todo List API")

todos: list[TodoResponse] = []
next_id = 1


@app.post(
    "/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED
)
def create_todo(todo: TodoCreate):
    global next_id

    new_todo = TodoResponse(
        id=next_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        priority=todo.priority
    )

    todos.append(new_todo)
    next_id += 1

    return new_todo


@app.get("/todos", response_model=list[TodoResponse])
def get_todos(
    completed: bool | None = Query(default=None),
    priority: str | None = Query(default=None)
):
    result = todos

    if completed is not None:
        result = [todo for todo in result if todo.completed == completed]

    if priority is not None:
        result = [todo for todo in result if todo.priority == priority]

    return result

@app.get("/todos/count" , response_model=int)
def get_count():
    return len(todos)

@app.get("/todos/completed", response_model=list[TodoResponse])
def get_completed_todos():
    return [todo for todo in todos if todo.completed]


@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo not found"
    )


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_data: TodoUpdate):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:

            updated_todo = TodoResponse(
                id=todo.id,
                title=todo_data.title,
                description=todo_data.description,
                completed=todo_data.completed,
                priority=todo_data.priority
            )

            todos[index] = updated_todo

            return updated_todo

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo not found"
    )


@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo not found"
    )