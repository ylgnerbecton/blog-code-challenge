## 🧾 Code Challeng

Backend API for managing blog posts and comments. Built with FastAPI and Python 3.11, following a clean and modular architecture.


---

### 🚀 Tech Stack

* Python 3.11
* FastAPI
* SQLAlchemy
* Alembic
* Poetry
* Pytest
* Pre-commit + Linters

---

### 🏗️ Architecture Overview

This project follows a Clean Modular Architecture with clear boundaries and responsibilities across layers. It draws inspiration from Domain-Driven Design (DDD) and Service-Oriented patterns.

Each module is designed to be testable, decoupled, and self-contained.

---

### 📦 Requirements

* Python 3.11+
* [Poetry](https://python-poetry.org/docs/#installation)

---

### ⚙️ Setup

```bash
cd backoffice-backend

make install
```

---

### ▶️ Running the API

```bash
make run
```

Access the Swagger UI at:

```
http://0.0.0.0:8000/docs
```

---

### 🧪 Running Tests

The test suite is structured into layers:

```
tests/
├── unit/              Unit tests for entities, services, and repositories
├── integration/       Full API tests with HTTP and database interaction
```

Run all tests with:

```bash
make test
```

Run a specific test suite:

```bash
pytest tests/unit
pytest tests/integration
```

---

### ✅ Code Quality – Pre-commit

This project uses [Pre-commit](https://pre-commit.com/) to enforce code quality with:

* `black`
* `isort`
* `flake8`
* `ruff`

Hooks are installed automatically via `make install`.

---

#### 🧹 Run Pre-commit manually

```bash
make lint
```

#### 🎨 Format Codebase

Automatically format all code with `black` and `isort`:

```bash
make format
```
