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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
