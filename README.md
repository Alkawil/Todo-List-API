# Todo-List-API
A RESTful API built with Flask for managing a Todo List application. Users can register, login, and perform CRUD operations on their todos.

## Features

- **RESTful API**: The API follows REST principles to manage resources (todos) using standard HTTP methods.
- **User Authentication**: Users can register and login with JWT (JSON Web Token) for secure access to their todo data.
- **CRUD Operations**: Perform **Create**, **Read**, **Update**, and **Delete** operations on todo items.
- **SQLite Database**: The data is stored in a lightweight SQLite database, which is easily scalable and manageable for small applications.
- **Data Modeling**: The app uses **Flask-SQLAlchemy** to define models for `User` and `Todo` entities, creating relationships between users and their todo items.

## Technologies Used

- **Flask**: Python web framework for building the API.
- **SQLite**: Lightweight database for storing user and todo information.
- **Flask-SQLAlchemy**: ORM for handling SQLite database interactions.
- **Flask-JWT-Extended**: For managing JSON Web Tokens (JWT) for authentication.
- **Python 3**: Programming language used for development.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Alkawil/Todo-List-API.git
