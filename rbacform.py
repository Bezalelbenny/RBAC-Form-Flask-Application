from flask import Flask, render_template, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rbac.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Required Database Extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# =====================================================================
# DATABASE MODELS (Flask-SQLAlchemy)
# =====================================================================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False) 
    role = db.Column(db.String(20), nullable=False)     

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)

# =====================================================================
# FORMS (Flask-WTF Forms)
# =====================================================================
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Save')

# =====================================================================
# BULLETPROOF DATABASE INITIALIZATION (Runs once at server startup)
# =====================================================================
with app.app_context():
    db.create_all() # This forces SQLite to physically build the tables immediately
    
    # Check and seed preset users
    if not User.query.filter_by(username='admin').first():
        db.session.add(User(username='admin', password='admin123', role='Admin'))
        db.session.add(User(username='editor', password='editor123', role='Editor'))
        db.session.add(User(username='viewer', password='viewer123', role='Viewer'))
        
    # Check and seed preset tasks
    if Task.query.count() == 0:
        db.session.add(Task(title='Preset Task One', description='Review basic RBAC authorization barriers.', author='admin'))
        db.session.add(Task(title='Preset Task Two', description='Confirm viewer read-only interface locks.', author='editor'))
        
    db.session.commit()

# =====================================================================
# ROUTES & CRUD LOGIC (Flask Routing)
# =====================================================================
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if user:
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        return '<h3>Invalid Credentials. <a href="/login">Try Again</a></h3>'
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session: return redirect(url_for('login'))
    tasks = Task.query.all()
    return render_template('dashboard.html', tasks=tasks, role=session['role'], user=session['username'])

@app.route('/task/new', methods=['GET', 'POST'])
def create_task():
    if 'username' not in session: return redirect(url_for('login'))
    if session['role'] not in ['Admin', 'Editor']: 
        return '<h2>403 - Forbidden: Access Denied</h2>', 403
        
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(title=form.title.data, description=form.description.data, author=session['username'])
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('task.html', form=form, title="Create Task")

@app.route('/task/edit/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    if 'username' not in session: return redirect(url_for('login'))
    if session['role'] not in ['Admin', 'Editor']: 
        return '<h2>403 - Forbidden: Access Denied</h2>', 403
        
    task = Task.query.get_or_404(id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('task.html', form=form, title="Edit Task")

@app.route('/task/delete/<int:id>', methods=['POST'])
def delete_task(id):
    if 'username' not in session: return redirect(url_for('login'))
    if session['role'] != 'Admin': 
        return '<h2>403 - Forbidden: Access Denied</h2>', 403
        
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)