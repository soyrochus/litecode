# LiteCode is a lightweight Python stack for accelerated development of applications and services
#
# Though Litecode, "Single" is the new "Full" stack. Using FastAPI and NiceGUI to build
# web applications entirely on the server side, Litecode removes the need for client-side
# JavaScript or TypeScript, while complexity is reduced by using a simplified architecture
# and single language for the entire stack.
#
# License: MIT License
# For the full license text, please refer to the LICENSE file in the root of the project.
#
# Copyright (c) 2024 Iwan van der Kleijn


from sqlalchemy.orm import Session
from .models import Task
from .database import dbsession

class TaskNotFoundError(Exception):
    def __init__(self, task_id):
        self.task_id = task_id
        super().__init__(f"Task with id {task_id} not found.")

@dbsession
def get_tasks(_session: Session):
    return _session.query(Task).all()

@dbsession
def add_task(task_data, _session: Session):
    new_task = Task(**task_data)
    _session.add(new_task)
    _session.commit()
    _session.refresh(new_task)
    return new_task

@dbsession
def update_task(task_id, task_data, _session: Session):
    task = _session.query(Task).filter(Task.id == task_id).first()
    if task:
        for key, value in task_data.items():
            setattr(task, key, value)
        _session.commit()
        _session.refresh(task)
    return task

@dbsession
def delete_task(task_id, _session: Session) -> None:
    task = _session.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise TaskNotFoundError(task_id)
    
    _session.delete(task)
    _session.commit()
   
 
@dbsession
def get_task(task_id: int, _session:Session):
    return _session.query(Task).filter(Task.id == task_id).first()