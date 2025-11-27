#  🟣🤖 HBnB Project: Cyberpunk Edition 🤖🟣

## ⚡ Project Overview
A full-stack, Cyberpunk-themed accommodation platform for booking futuristic lodging across a dystopian landscape. Across four major evolutions, the project transforms from system architecture, to backend logic, to database integration and authentication, and finally, to building the user interface. This project was completed as part of the Holberton School curriculum, and inspired by Airbnb.

## 🧬 Project Evolution 
The project is divided into four major parts, each building on the previous version:
- <b>Part 1: System Architecture</b>  
Technical documentation and UML diagrams providing a high-level overview of the system's architecture.  
Jump to  👉 [Part 1 README](part1/README.md)

- <b>Part 2: API and Business Logic Layer</b>  
Implementation of the core business logic, models, and an in-memory repository used to simulate data persistence during early development.  
Jump to 👉 [Part 2 README](part2/README.md)

- <b>Part 3: Authentication and Database</b>  
Implementation of JWT-based authentication, and migration from in-memory storage to SQLAlchemy and SQLite for data persistence.  
Jump to 👉 [Part 3 README](part3/README.md)

- <b>Part 4: Simple Web Client</b>  
Implementation of HTML, CSS, and vanilla JavaScript connected to the backend, enabling user interaction, authentication and review submission.  
Jump to 👉 [Part 4 README](part4/README.md)

## 📡Tech Stack
- Python
- Flask
- Flask-RESTX
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Bcrypt
- Flask-JWT-Extended
- Pytest
- Flask-cors
- SQLite
- HTML
- CSS
- JavaScript (vanilla)

## 🚀 Getting Started
### Clone the repository
```bash
git clone https://github.com/Anna-Halaapiapi/holbertonschool-hbnb.git
cd holbertonschool-hbnb
```
### Create a virtual environment 
```bash
python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```
### Install the dependencies
```bash
cd part3
pip install -r requirements.txt
```
### Initialize the database
```bash
python3 run.py

# The server will start on http://127.0.0.1:5000/.
# The SQLite database (development.db) and tables will be created in this step
```
### End database initialization
```bash
CTRL + C
```
### Seed the initial data into database
```bash
sqlite3 instance/development.db < p4_seed_file.sql
# This will seed the following data into the database:
# admin user
# four places
```
### Run the application normally
```bash
python3 run.py
```

## 👥 Contributors
👾 Madison Fleming  
👾 Toni Mathieson  
👾 Ashleigh Henna  
👾 Anna Halaapiapi
