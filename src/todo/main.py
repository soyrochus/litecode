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

from fastapi import FastAPI
from nicegui import ui
from todo import models
from sqlalchemy.orm import Session
from datetime import datetime
from todo.controllers import get_task, get_tasks, add_task, update_task, delete_task
from todo.database import get_db

fastapi_app = FastAPI()

def open_add_task_dialog():
    create_task_dialog("Add New Task", None, save_task)


def delete_task_action(task_id):
    # Delete the task from 
    # the database
    delete_task(task_id)
    
    # Notify the user and refresh the table
    ui.notify(f"Task {task_id} deleted")
    update_task_table()


def save_edited_task(
    dialog,
    task_id,
    title_input,
    description_input,
    due_date_input,
    priority_input,
    category_input,
    completed_input
):
    task_data = {
        "title": title_input.value,
        "description": description_input.value,
        "due_date": datetime.strptime(due_date_input.value, "%Y-%m-%d") if due_date_input.value else None,
        "priority": int(priority_input.value) if priority_input.value else None,
        "category": category_input.value,
        "completed": completed_input.value,
    }
    
    # Update the task in the database
    update_task(task_id, task_data)
    
    # Close the dialog and refresh the table
    dialog.close()
    ui.notify("Task updated")
    update_task_table()


def open_edit_task_dialog(task_id):

    # Retrieve the task based on the ID
    task = get_task(task_id)
    if not task:
        ui.notify("Task not found")
        return
    
    # Open the dialog to edit the task
    with ui.dialog() as dialog:
        with ui.card():

            ui.label("Edit Task").classes("text-h5")
            title_input = ui.input("Title", value=task.title)
            description_input = ui.input("Description", value=task.description)
            due_date_input = ui.input("Due Date (YYYY-MM-DD)", value=task.due_date.strftime("%Y-%m-%d") if task.due_date else "")
            priority_input = ui.number("Priority", value=task.priority)
            category_input = ui.input("Category", value=task.category)
            completed_input = ui.switch("Completed", value=task.completed)

            # Save button to apply changes
            ui.button(
                "Save",
                on_click=lambda: save_edited_task(
                    dialog,
                    task_id,
                    title_input,
                    description_input,
                    due_date_input,
                    priority_input,
                    category_input,
                    completed_input
                )
            )
            ui.button("Cancel", on_click=dialog.close)
    dialog.open()


def save_task(dialog, task_data):
    add_task(task_data)
    dialog.close()
    ui.notify("Task added")
    update_task_table()  # Only refresh the table, not the whole page

def update_task_table():
    tasks = get_tasks()
    task_table = create_task_table()
    update_table_rows(task_table, tasks)

def create_task_dialog(title, task_data=None, save_action=None):
    with ui.dialog() as dialog:
        with ui.card():
            ui.label(title).classes("text-h5")
            title_input = ui.input("Title", value=task_data.get("title") if task_data else "")
            description_input = ui.input("Description")
            due_date_input = ui.input("Due Date (YYYY-MM-DD)")
            priority_input = ui.number("Priority")
            category_input = ui.input("Category")
            completed_input = ui.switch("Completed")
            ui.button(
                "Save",
                on_click=lambda: save_action(dialog, {
                    "title": title_input.value,
                    # Collect other field values here
                }),
            )
            ui.button("Cancel", on_click=dialog.close)
    dialog.open()


@ui.page("/")
def index():

    with ui.column().classes("w-full"):
        ui.label("TODO List App").classes("text-h4")
        ui.button("Add New Task", on_click=open_add_task_dialog)
        ui.separator()

        # Refactored task table function
        task_table = create_task_table()
        task_table.update()

def create_task_table():
    tasks = get_tasks()
    with ui.table(
        columns=[
            {"name": "id", "label": "Id", "field": "id"},
            {"name": "title", "label": "Title", "field": "title"},
            {"name": "due_date", "label": "Due Date", "field": "due_date"},
            {"name": "priority", "label": "Priority", "field": "priority"},
            {"name": "category", "label": "Category", "field": "category"},
            {"name": "completed", "label": "Completed", "field": "completed"},
            {"name": "actions", "label": "Actions"},
        ],
        rows=[]
    ).classes("w-full") as task_table:
        # Add Edit and Delete buttons to each row
        task_table.add_slot('body-cell-actions', """
        <q-td :props="props">
            <q-btn @click="$parent.$emit('edit_task', props.row)" icon="edit" flat />
            <q-btn @click="$parent.$emit('delete_task', props.row)" icon="delete" flat />
        </q-td>
        """)
        # Bind events to Edit and Delete actions
        task_table.on('edit_task', lambda msg: open_edit_task_dialog(msg.args['id']))
        task_table.on('delete_task', lambda msg: delete_task_action(msg.args['id']))
        update_table_rows(task_table, tasks)

    return task_table

def update_table_rows(task_table, tasks):
    task_table.rows.clear()
    for task in tasks:
        task_table.rows.append({
            "id": task.id,
            "title": task.title,
            "due_date": task.due_date.strftime("%Y-%m-%d") if task.due_date else "",
            "priority": task.priority or "",
            "category": task.category or "",
            "completed": "✅" if task.completed else "⬜",
        })
    task_table.update()


