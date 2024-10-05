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

from fastapi.testclient import TestClient
from todo.view import fastapi_app
from todo import actions, models, database

client = TestClient(fastapi_app)


# def test_read_main():
#     response = client.get("/")
#     assert response.status_code == 200


def test_add_task():
    session = database.SessionLocal()
    initial_count = session.query(models.Task).count()
    task_data = {
        'title': 'Test Task',
        'description': 'Test Description',
        'due_date': None,
        'priority': 1,
        'category': 'Test',
        'completed': False
    }
    actions.add_task(task_data, _session=session)
    new_count = session.query(models.Task).count()
    assert new_count == initial_count + 1
