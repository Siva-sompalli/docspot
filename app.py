import os
from flask import Flask, render_template, request, redirect, render_template_string
from models import db, User, Doctor, Appointment

# -------- BASE DIRECTORY FIX --------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -------- FLASK APP --------
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)

# -------- DATABASE CONFIG --------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///docspot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret123'

db.init_app(app)

# -------- HOME --------
@app.route('/')
def home():
    return "DocSpot App with Database Connected"

# -------- REGISTER --------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        user = User(name=name, email=email, password=password, role='patient')
        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

# -------- LOGIN --------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            return redirect('/doctors')
        else:
            return "Invalid Login"

    return render_template('login.html')


# -------- DOCTORS LIST (NO TEMPLATE ERROR) --------
@app.route('/doctors')
def doctors():
    doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors)


# -------- BOOK APPOINTMENT --------
@app.route('/book/<doctor>', methods=['GET', 'POST'])
def book(doctor):
    if request.method == 'POST':
        patient = request.form['patient']
        date = request.form['date']

        appointment = Appointment(
            patient_name=patient,
            doctor_name=doctor,
            date=date
        )

        db.session.add(appointment)
        db.session.commit()

        return "Appointment Booked Successfully"

    return render_template('book.html', doctor=doctor)

# -------- VIEW APPOINTMENTS --------
@app.route('/appointments')
def appointments():
    appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=appointments)


# -------- RUN APP --------
if __name__ == '__main__':
    app.run(debug=True)
