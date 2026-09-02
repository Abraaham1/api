from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    completed: bool = False
    priority: str = "medium"


class TodoUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    completed: bool = False
    priority: str = "medium"


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    priority: str