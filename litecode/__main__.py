
from fastapi import FastAPI
from nicegui import ui, app as nicegui_app
from . import models, database
from sqlalchemy.orm import Session
from datetime import datetime

# Initialize FastAPI app
fastapi_app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper functions for database operations
def get_tasks(db: Session):
    return db.query(models.Task).all()

def add_task(db: Session, task_data):
    new_task = models.Task(**task_data)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def update_task(db: Session, task_id, task_data):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        for key, value in task_data.items():
            setattr(task, key, value)
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return task

# NiceGUI UI components
@ui.page("/")
def index():
    db = next(get_db())
    tasks = get_tasks(db)

    with ui.column().classes('w-full'):
        ui.label('TODO List App').classes('text-h4')
        ui.button('Add New Task', on_click=open_add_task_dialog)
        ui.separator()

        with ui.table(columns=[
            {'name': 'title', 'label': 'Title', 'field': 'title'},
            {'name': 'due_date', 'label': 'Due Date', 'field': 'due_date'},
            {'name': 'priority', 'label': 'Priority', 'field': 'priority'},
            {'name': 'category', 'label': 'Category', 'field': 'category'},
            {'name': 'completed', 'label': 'Completed', 'field': 'completed'},
            {'name': 'actions', 'label': 'Actions'}
        ], rows=[]).classes('w-full') as task_table:

            def refresh_table():
                tasks = get_tasks(db)
                task_table.rows.clear()
                for task in tasks:
                    task_table.rows.append({
                        'title': task.title,
                        'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else '',
                        'priority': task.priority or '',
                        'category': task.category or '',
                        'completed': 'Yes' if task.completed else 'No',
                        'actions': ui.button('Edit', on_click=lambda e, task_id=task.id: open_edit_task_dialog(task_id)).classes('mr-2') +
                                   ui.button('Delete', on_click=lambda e, task_id=task.id: delete_task_action(task_id))
                    })
                task_table.update()

            refresh_table()

def open_add_task_dialog():
    with ui.dialog() as dialog:
        with ui.card():
            ui.label('Add New Task').classes('text-h5')
            title_input = ui.input('Title')
            description_input = ui.input('Description')
            due_date_input = ui.input('Due Date (YYYY-MM-DD)')
            priority_input = ui.number('Priority')
            category_input = ui.input('Category')
            completed_input = ui.switch('Completed')
            ui.button('Save', on_click=lambda: save_task(dialog, title_input, description_input, due_date_input, priority_input, category_input, completed_input))
            ui.button('Cancel', on_click=dialog.close)
    dialog.open()

def save_task(dialog, title_input, description_input, due_date_input, priority_input, category_input, completed_input):
    db = next(get_db())
    task_data = {
        'title': title_input.value,
        'description': description_input.value,
        'due_date': datetime.strptime(due_date_input.value, '%Y-%m-%d') if due_date_input.value else None,
        'priority': int(priority_input.value) if priority_input.value else None,
        'category': category_input.value,
        'completed': completed_input.value
    }
    add_task(db, task_data)
    dialog.close()
    ui.notify('Task added')
    index()  # Refresh the page to show updated tasks

def open_edit_task_dialog(task_id):
    db = next(get_db())
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        ui.notify('Task not found')
        return

    with ui.dialog() as dialog:
        with ui.card():
            ui.label('Edit Task').classes('text-h5')
            title_input = ui.input('Title', value=task.title)
            description_input = ui.input('Description', value=task.description)
            due_date_input = ui.input('Due Date (YYYY-MM-DD)', value=task.due_date.strftime('%Y-%m-%d') if task.due_date else '')
            priority_input = ui.number('Priority', value=task.priority)
            category_input = ui.input('Category', value=task.category)
            completed_input = ui.switch('Completed', value=task.completed)
            ui.button('Save', on_click=lambda: save_edited_task(dialog, task_id, title_input, description_input, due_date_input, priority_input, category_input, completed_input))
            ui.button('Cancel', on_click=dialog.close)
    dialog.open()

def save_edited_task(dialog, task_id, title_input, description_input, due_date_input, priority_input, category_input, completed_input):
    db = next(get_db())
    task_data = {
        'title': title_input.value,
        'description': description_input.value,
        'due_date': datetime.strptime(due_date_input.value, '%Y-%m-%d') if due_date_input.value else None,
        'priority': int(priority_input.value) if priority_input.value else None,
        'category': category_input.value,
        'completed': completed_input.value
    }
    update_task(db, task_id, task_data)
    dialog.close()
    ui.notify('Task updated')
    index()  # Refresh the page

def delete_task_action(task_id):
    db = next(get_db())
    delete_task(db, task_id)
    ui.notify('Task deleted')
    index()  # Refresh the page

# Run the NiceGUI app with FastAPI
if __name__ == '__main__':
    print(__name__)
    ui.run_with(fastapi_app)

