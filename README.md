# TodoApp Documentation

## Overview
TodoApp is a **FastAPI-based application** with JWT authentication, role-based access control, and SQLite database integration.  
Users can register, log in, manage their todos, and update their profiles. Admins have elevated privileges to view all todos.

---

## Features
- User Authentication using JWT  
- Role-based Authorization (**User & Admin**)  
- Create, Read, Update, and Delete todos  
- User profile management (edit, change password, delete account)  
- Admin endpoint to view all todos  
- SQLite database with SQLAlchemy ORM  

---

## Tech Stack
- **Backend**: FastAPI  
- **Database**: SQLite  
- **ORM**: SQLAlchemy  
- **Authentication**: OAuth2 + JWT (python-jose, passlib)  
- **Validation**: Pydantic  
- **Server**: Uvicorn  

---

## Project Structure
TodoApp/
│── routers/
│ ├── auth.py # User registration, login, JWT handling
│ ├── todo.py # CRUD operations for todos
│ ├── admin.py # Admin-only endpoints
│ ├── users.py # User profile & password management
│
│── main.py # App entry point
│── database.py # DB engine & session
│── models.py # SQLAlchemy models

----

