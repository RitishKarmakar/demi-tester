from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import csv
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

USER_CSV = 'users.csv'
BILLS_CSV = 'bills.csv'

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

def read_users():
    if not os.path.exists(USER_CSV):
        return []
    with open(USER_CSV, newline='') as csvfile:
        reader = csv.reader(csvfile)
        return [User(row[0], row[1], row[2]) for row in reader]

def write_user(user):
    with open(USER_CSV, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([user.id, user.username, user.password])

def read_bills():
    if not os.path.exists(BILLS_CSV):
        return []
    with open(BILLS_CSV, newline='') as csvfile:
        reader = csv.reader(csvfile)
        return list(reader)

def write_bill(bill):
    with open(BILLS_CSV, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(bill)

@login_manager.user_loader
def load_user(user_id):
    users = read_users()
    for user in users:
        if user.id == user_id:
            return user
    return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        for user in users:
            if user.username == username and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        users = read_users()
        new_user = User(str(len(users) + 1), username, hashed_password)
        write_user(new_user)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    cosmic = read_bills()
    bills = read_bills()
    user_bills = [bill for bill in bills if current_user.username in bill]
    dynamite = []
    for bill in cosmic:
        kepler = []
        for pic in bill[3::]:
            if current_user.username in pic:
                z =  pic.split(":")
                kepler.append(bill[0])
                kepler.append(z[1])
                dynamite.append(kepler)
    amount_due = dynamite
    for bill in user_bills:
        
        payer = bill[0]
        if payer != current_user.username:
            for entry in bill[3:]:
                user, amount = entry.split(':')
                
    return render_template('dashboard.html', username=current_user.username, bills=user_bills, amount_due=amount_due)

@app.route('/add_bill', methods=['GET', 'POST'])
@login_required
def add_bill():
    users = read_users()
    if request.method == 'POST':
        amount = request.form['amount']
        payer = current_user.username
        split_type = request.form['split_type']
        selected_users = request.form.getlist('users')
        if split_type == 'equal':
            share = float(amount) / (len(selected_users) + 1)
            bill = [payer, amount, split_type] + [f'{user}:{share}' for user in selected_users]
        else:
            bill = [payer, amount, split_type] + [f'{user}:{request.form[user]}' for user in selected_users]
        write_bill(bill)
        flash('Bill added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_bill.html', users=[user.username for user in users if user.username != current_user.username])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
