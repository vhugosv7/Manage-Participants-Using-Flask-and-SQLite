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
- Bootstrap 5.02

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
   python app.p

5. Open your browser and navigate to http://127.0.0.1:5000/ to interact with the application.


### Screnshoots


![Main Page](https://github.com/user-attachments/assets/5b31bc8f-020e-45ea-aa4c-9d7fbdb73373)


![Add new participant](https://github.com/user-attachments/assets/3b757650-6b4b-4d2f-9272-05a545f859c8)


![All participants table](https://github.com/user-attachments/assets/1c2698a9-838b-44e6-ab69-fe2a79176cbf)


![Update participant information. (Infomartion is displayed in input field)](https://github.com/user-attachments/assets/b2376de1-2b16-4cc6-b8ab-550bc1949dcc)


![Action executed succesfully screen](https://github.com/user-attachments/assets/a11a3135-d918-4ce7-91ee-abe16f115140)


![Action no executed screen](https://github.com/user-attachments/assets/6469779e-e655-4db3-865c-809953e1e8bb)


![Error 404 (Page not found)](https://github.com/user-attachments/assets/98411e93-9dd7-4596-b75f-84b2381fd1ac)


