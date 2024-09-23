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

import pytest
from fastapi.testclient import TestClient
from app.main import fastapi_app
from app import models, database

client = TestClient(fastapi_app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

def test_add_task():
    db = database.SessionLocal()
    initial_count = db.query(models.Task).count()
    task_data = {
        'title': 'Test Task',
        'description': 'Test Description',
        'due_date': None,
        'priority': 1,
        'category': 'Test',
        'completed': False
    }
    models.add_task(db, task_data)
    new_count = db.query(models.Task).count()
    assert new_count == initial_count + 1
