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
from datetime import datetime
from todo.actions import get_task, get_tasks, add_task, update_task, delete_task

fastapi_app = FastAPI()


def open_task_dialog(task_id=None):
    """Open the dialog for adding or editing a task."""
    task_data = get_task(task_id) if task_id else None

    title = "Edit Task" if task_id else "Add New Task"

    with ui.dialog() as dialog:
        with ui.card():
            ui.label(title).classes("text-h5")
            title_input = ui.input("Title", value=task_data.title if task_data else "")
            description_input = ui.input("Description", value=task_data.description if task_data else "")
            due_date_input = ui.input(
                "Due Date (YYYY-MM-DD)",
                value=task_data.due_date.strftime("%Y-%m-%d") if task_data and task_data.due_date else "",
            )
            priority_input = ui.number("Priority", value=task_data.priority if task_data else None)
            category_input = ui.input("Category", value=task_data.category if task_data else "")
            completed_input = ui.switch("Completed", value=task_data.completed if task_data else False)

            # Save button to apply changes
            ui.button(
                "Save",
                on_click=lambda: save_task_from_dialog(
                    dialog,
                    task_id,
                    title_input,
                    description_input,
                    due_date_input,
                    priority_input,
                    category_input,
                    completed_input,
                ),
            )
            ui.button("Cancel", on_click=dialog.close)
    dialog.open()


def delete_task_action(task_id):
    # Delete the task from the database
    delete_task(task_id)

    # Notify the user and refresh the table
    ui.notify(f"Task {task_id} deleted")
    create_task_table.refresh()


def save_task_from_dialog(
    dialog,
    task_id,
    title_input,
    description_input,
    due_date_input,
    priority_input,
    category_input,
    completed_input,
):
    task_data = {
        "title": title_input.value,
        "description": description_input.value,
        "due_date": (
            datetime.strptime(due_date_input.value, "%Y-%m-%d") if due_date_input.value else None
        ),
        "priority": int(priority_input.value) if priority_input.value else None,
        "category": category_input.value,
        "completed": completed_input.value,
    }

    if task_id:
        # Update the task in the database
        update_task(task_id, task_data)
        ui.notify("Task updated")
    else:
        # Add the task to the database
        add_task(task_data)
        ui.notify("Task created")

    # Close the dialog and refresh the table
    dialog.close()
    create_task_table.refresh()  # Only refresh the table, not the whole page


@ui.page("/")
def index():
    with ui.column().classes("w-full"):
        ui.label("TODO List App").classes("text-h4")
        ui.button("Add New Task", on_click=lambda: open_task_dialog())
        ui.separator()
        create_task_table()


@ui.refreshable
def create_task_table():
    tasks = get_tasks()
    task_table = ui.table(
        columns=[
            {"name": "id", "label": "Id", "field": "id"},
            {"name": "title", "label": "Title", "field": "title"},
            {"name": "due_date", "label": "Due Date", "field": "due_date"},
            {"name": "priority", "label": "Priority", "field": "priority"},
            {"name": "category", "label": "Category", "field": "category"},
            {"name": "completed", "label": "Completed", "field": "completed"},
            {"name": "actions", "label": "Actions"},
        ],
        rows=[],
    ).classes("w-full")

    # Add actions to rows
    task_table.add_slot(
        "body-cell-actions",
        """
    <q-td :props="props">
        <q-btn @click="$parent.$emit('edit_task', props.row)" icon="edit" flat />
        <q-btn @click="$parent.$emit('delete_task', props.row)" icon="delete" flat />
    </q-td>
    """,
    )

    task_table.on("edit_task", lambda msg: open_task_dialog(msg.args["id"]))
    task_table.on("delete_task", lambda msg: delete_task_action(msg.args["id"]))

    update_table_rows(task_table, tasks)
    return task_table


def update_table_rows(task_table, tasks):
    task_table.rows.clear()
    for task in tasks:
        task_table.rows.append(
            {
                "id": task.id,
                "title": task.title,
                "due_date": task.due_date.strftime("%Y-%m-%d") if task.due_date else "",
                "priority": task.priority or "",
                "category": task.category or "",
                "completed": "✅" if task.completed else "⬜",
            }
        )
    task_table.update()
