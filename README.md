# Litecode

## Introduction

LiteCode is a lightweight Python stack for accelerated development of applications and services.

Though Litecode, "Single" is the new "Full" stack. Using FastAPI and NiceGUI to build 
web applications entirely on the server side, Litecode removes the need for client-side 
JavaScript or TypeScript, while complexity is reduced by using a simplified architecture 
and single language for the entire stack.

## Lite Code TODO List App

This is a simple TODO List application built using the Lite Code stack:

- **Python (100%)**
- **FastAPI** for backend logic
- **NiceGUI** for server-side UI rendering
- **Poetry** as the package manager
- **Pytest** for testing

## Setup instructions

### Prerequisites

- Python 3.12
- Poetry (for dependency management)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/soyrochus/litecode.git
cd litecode
```

2. Install dependencies using Poetry:

```bash
poetry install
```


### Testing

To run tests:

```bash
poetry run pytest
```

### Run all checks

To run all checks:

```bash
poetry run check-all
```

This will run black, flake8, mypy and pytest, cosequetively

## Copyright and License

Copyright (c) 2024 Iwan van der Kleijn

License: MIT License

For the full license text, please refer to the LICENSE file in the root of the project.

