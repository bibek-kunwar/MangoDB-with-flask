from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for flash messages

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017")
db = client['mydatabase']
collection = db['students']

if client:
    print("Mongo Connected")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get data from the form
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        facility = request.form.get('facility')
        contact1 = request.form.get('contact1')
        contact2 = request.form.get('contact2')
        email = request.form.get('email')

        # Validate data (you can add more validation as needed)
        if not fname or not lname:
            flash('First Name and Last Name are required.', 'error')
        else:
            # Generate a unique ID for the student
            student_id = str(uuid.uuid4())

            students = {
                'id': student_id,
                'fname': fname,
                'lname': lname,
                'facility': facility,
                'contact': {
                    'contact1': contact1,
                    'contact2': contact2
                },
                'email': email 
            }

            collection.insert_one(students)
            flash('Student added successfully.', 'success')

    students = collection.find()
    return render_template('index.html', students=students)

@app.route('/edit_student/<student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if request.method == 'POST':
        # Get data from the form
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        facility = request.form.get('facility')
        contact1 = request.form.get('contact1')
        contact2 = request.form.get('contact2')
        email = request.form.get('email')

        # Validate data (you can add more validation as needed)
        if not fname or not lname:
            flash('First Name and Last Name are required.', 'error')
        else:
            collection.update_one(
                {'id': student_id},
                {
                    '$set': {
                        'fname': fname,
                        'lname': lname,
                        'facility': facility,
                        'contact.contact1': contact1,
                        'contact.contact2': contact2,
                        'email': email
                    }
                }
            )

            flash('Student updated successfully.', 'success')

    student = collection.find_one({'id': student_id})
    return render_template('edit_student.html', student=student)

@app.route('/delete_student/<student_id>', methods=['POST'])
def delete_student(student_id):
    collection.delete_one({'id': student_id})
    flash('Student deleted successfully.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
