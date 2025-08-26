from flask import Flask, render_template, request
import sqlite3

# Change the template folder path, according to your path.
app = Flask(__name__)


@app.route('/')  # Main Route - index
def index():
    return render_template('index.html')


connect = sqlite3.connect('database.db')
connect.execute('''CREATE TABLE IF NOT EXISTS PARTICIPANTS
                (id_participant INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,
                email TEXT, city TEXT, country TEXT, phone TEXT)''')


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        city = request.form['city']
        country = request.form['country']
        phone = request.form['phone']
        # Avoiding names with less or equal than one character
        if len(name) <= 1:
            print("Name field must be more than 1 character.", name)
            return no_action()
        else:
            with sqlite3.connect("database.db") as users:
                cursor = users.cursor()
                cursor.execute('''INSERT INTO PARTICIPANTS
                               (name,email,city,country,phone)
                               VALUES (?,?,?,?,?)''',
                               (name, email, city, country, phone))
                users.commit()
        return action()
    else:
        return render_template('join.html')


@app.route('/participants')
def participants():
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM PARTICIPANTS')

    data = cursor.fetchall()
    #  Get the total number of participants stored
    count = ('''select count(name) from PARTICIPANTS''')
    cursor.execute(count)
    count = cursor.fetchall()
    my_string = ",".join(str(element) for element in count)
    my_string = my_string.replace(',', '')
    print("this is the total participants count", my_string)
    return render_template("participants.html", data=data, my_string=my_string)


@app.route('/find', methods=['POST', 'GET'])
def find():

    if request.method == 'POST':
        id_participant = request.form.get('id_participant')
        print(id_participant, "find function")
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(f'''SELECT * FROM PARTICIPANTS where
                       id_participant={id_participant}''')
        data_find = cursor.fetchall()
        if len(data_find) == 0:  # if the id does not exist,return error page
            return no_action()
        return render_template("find.html", data_find=data_find)
    else:
        return render_template("find.html")


@app.route('/delete', methods=['POST'])
def delete():
    # Get the participant ID from the hidden field 'id_from_table'
    participant_id = request.form.get('id_from_table')

    # Print the participant ID for debugging purposes
    print(f"Participant ID to delete: {participant_id}")

    # Use 'with' to connect to the SQLite database
    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()

        # SQL command to delete a particiapnt
        delete_query = '''
        DELETE FROM PARTICIPANTS
        WHERE id_participant = ?;
        '''

        # Name of the particiapnt to be deleted
        participant_id = participant_id

        # Execute the SQL command with the data
        cursor.execute(delete_query, (participant_id,))

        # Commit the changes to save the deletion
        connection.commit()

        # Print a confirmation message
        print(f"Deleted participant record for {participant_id}.")

    # Redirect
    return action()


@app.route('/update', methods=['POST'])
def update():
    # Get the participant ID data
    # Data for the update
    participant_id = request.form.get('id_participant_input')
    name = request.form.get('name_participant_input')
    email = request.form.get('email_input')
    city = request.form.get('city_input')
    country = request.form.get('country_input')
    phone = request.form.get('phone_input')

    # Print the participant ID for debugging purposes
    print(f'''TESTING:{participant_id}, {name},
          {email}, {city}, {country}, {phone}''')
    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()

        # SQL command to update
        update_query = '''
        UPDATE PARTICIPANTS
        SET name = ?,
        email = ?,
        city = ?,
        country = ?,
        phone = ?
        WHERE id_participant = ?;
        '''

        # Execute the SQL command with the data
        cursor.execute(update_query,
                       (name, email,
                        city, country, phone, participant_id))

        # Commit the changes to save the update
        connection.commit()

        # Print a confirmation message
        print(f"Data updated {participant_id} - {name}.")

        return action()


@app.route('/action')
def action():
    # Simulating an action being successfully executed
    success_message = "Action executed successfully!"
    # Rendering the template string with the success message
    return render_template('success.html', success_message=success_message)


@app.route('/error')
def no_action():
    # Simulating an action being successfully executed
    message = "The action was not executed !"
    # Rendering the template string with the success message
    return render_template('no_success.html', message=message)


@app.errorhandler(404)  # inbuilt function which takes error as parameter
def not_found(e):
    return render_template("no_page.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
