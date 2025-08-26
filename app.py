from flask import Flask, render_template, request, render_template_string
import sqlite3

# Change the template folder path, according to your path.
app = Flask(__name__, template_folder='Manage-Participants-Using-Flask-and-SQLite')


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

    # HTML template as a string
    template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="data:image/x-icon;base64,AAABAAEAEBAAAAEACABoBQAAFgAAACgAAAAQAAAAIAAAAAEACAAAAAAAAAEAAAAAAAAAAAAAAAEAAAAAAAAAAAAA////AACTsAACqswA/9GoANn//wDJmf8A2bj/AOj//wD/nEUA/7Z1AOvZ/wDUhkIAAND6APD//wD/wowAA9X/AP+pXgD/q2EAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQwIBQUFBQUFBAQSEhIMDAARCAgICAgIBQUEDw8SCQwADw4OCAgICAgFBAQPEhIJAAAODggICAgIBQQEDw8KCQAADg4ODggICAUEBAQPCQwAAA4ODg4OCAgIBQQEDwkAAAAODg4ODgsLCAUEBA8JAAAAAgICDgsGBgsFBA8PCQAAEBANAw4OAAAHBAQPDwkAAAALAA4OAQEABQQEDwoJAAAAAQAODg4AAAUEBA8JAAAAAAAODg4ODggFBA8PCQAAAAAACAgOCAUFBA8PDwkAAAAAAAAFBQUPDw8PCgkAAAAAAAAAAAQPDw8JCgkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAgAAAAMAAAADAAAAAwAEAAMABAADAAQAAgAEAAMABAADAAwAA4AMAAOADAADwBwAA+A8AAP//AAA=" rel="icon" type="image/x-icon">
        <title>Action Result</title>
        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    </head>
    <body>
        <div class="container mt-4">
            <!-- Success Message -->
            <div class="alert alert-success alert-dismissible fade show col text-center"
            role="alert">
                <strong>{{ success_message }}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="alert"
                aria-label="Close"></button>
            </div>
            <div class="conatiner mt-5">
                <h3 class="d-flex justify-content-center">Action Completed!
                </h3>
                <p class="d-flex justify-content-center">
                Your action was completed successfully.</p>
                <img  class="rounded mx-auto d-block"
                src="https://www.svgrepo.com/show/530196/crocodile.svg"
                alt="Success" width="200" height="300">
                <div class="col text-center">
                    <a href="/" class="btn btn-success ">Go Back Home</a>
                </div>
            </div>
        </div>
    <!-- Bootstrap JS and dependencies -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
     <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    '''

    # Rendering the template string with the success message
    return render_template_string(template, success_message=success_message)


@app.route('/error')
def no_action():
    # Simulating an action being successfully executed
    message = "The action was not executed !"

    # HTML template as a string
    template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="data:image/x-icon;base64,AAABAAEAEBAAAAEACABoBQAAFgAAACgAAAAQAAAAIAAAAAEACAAAAAAAAAEAAAAAAAAAAAAAAAEAAAAAAAAAAAAA////AACTsAACqswA/9GoANn//wDJmf8A2bj/AOj//wD/nEUA/7Z1AOvZ/wDUhkIAAND6APD//wD/wowAA9X/AP+pXgD/q2EAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQwIBQUFBQUFBAQSEhIMDAARCAgICAgIBQUEDw8SCQwADw4OCAgICAgFBAQPEhIJAAAODggICAgIBQQEDw8KCQAADg4ODggICAUEBAQPCQwAAA4ODg4OCAgIBQQEDwkAAAAODg4ODgsLCAUEBA8JAAAAAgICDgsGBgsFBA8PCQAAEBANAw4OAAAHBAQPDwkAAAALAA4OAQEABQQEDwoJAAAAAQAODg4AAAUEBA8JAAAAAAAODg4ODggFBA8PCQAAAAAACAgOCAUFBA8PDwkAAAAAAAAFBQUPDw8PCgkAAAAAAAAAAAQPDw8JCgkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAgAAAAMAAAADAAAAAwAEAAMABAADAAQAAgAEAAMABAADAAwAA4AMAAOADAADwBwAA+A8AAP//AAA=" rel="icon" type="image/x-icon">
        <title>Action Result</title>
        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    </head>
    <body>
        <div class="container mt-4">
            <!-- Success Message -->
            <div class="alert alert-danger alert-dismissible
            fade show col text-center" role="alert">
                <strong>{{message }}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="alert"
                aria-label="Close"></button>
            </div>
            <div class="conatiner mt-5">
            <h3 class="d-flex justify-content-center">Action No Completed!</h3>
                <p class="d-flex justify-content-center">An error occurred,
                and your action couldn't be completed. Please try again.</p>
                <!--<img  class="rounded mx-auto d-block" src="https://www.svgrepo.com/show/492592/confused.svg" alt="Success" width="200" height="300">-->
                <img  class="rounded mx-auto d-block" src="https://www.svgrepo.com/show/530193/polar-bear.svg" alt="Success" width="200" height="300">
                <div class="col text-center">
                    <a href="/" class="btn btn-outline-danger">Go Back</a>
                </div>

            </div>
        </div>
        <!-- Bootstrap JS and dependencies -->
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    '''
    # Rendering the template string with the success message
    return render_template_string(template, message=message)


@app.errorhandler(404)  # inbuilt function which takes error as parameter
def not_found(e):
    return render_template("no_page.html")


if __name__ == '__main__':
    app.run(debug=False)
