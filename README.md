# Web-App-Using-Flask-and-SQLite


This is a simple Flask web application that allows you to manage participants in a SQLite database. You can add new participants, delete existing ones, edit participant details, and view all participants.

## Features

- **Add Participants**: The `join()` function allows you to add new participants to the database.
- **View All Participants**: The `participants()` function displays all the participants that have registered in the system.
- **Find a Participant**: The `find()` function helps you search for a specific participant in the database.
- **Delete a Participant**: The `delete()` function allows you to remove a participant from the database.
- **Update Participant Details**: The `update()` function lets you edit details of a registered participant.
- **Action Status**: The `action()` function is shown when an action (add, delete, update) is successfully executed.
- **No Action Status**: The `no_action()` function is shown when no action is performed or if an error occurs.

## Installation

Follow the steps below to set up and run this project locally.

### Prerequisites

- Python 3.11.7
- Flask 2.2.5
- SQLite (Database is handled automatically)
- Install the required dependencies using `pip`

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/vhugosv7/Web-App-Using-Flask-and-SQLite.git

2. Navigate to the project folder:
   ```bash
   cd Web-App-Using-Flask-and-SQLite

3. Install the required dependencies:
  ```bash
   pip install -r requirements.txt

4. Run the Flask application:
   ```bash
  python app.py


5. Open your browser and navigate to http://127.0.0.1:5000/ to interact with the application.
