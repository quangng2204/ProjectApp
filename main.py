from flask import Flask, render_template, flash, session, request
from werkzeug.utils import redirect
from forms import SignUpForm, SignInForm, TaskForm, ProjectForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'QuangNvh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models

@app.route('/')
def main():
    todolist = [
        {
            'name': 'Buy milk',
            'description': 'Buy 2 liter of milk in Coopmart.'
        },
        {
            'name': 'Get money',
            'description': 'Get 500k from ATM'
        }
    ]
    return render_template('index.html', todolist=todolist)

@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
    form = SignInForm()

    if form.validate_on_submit():
        _email = form.inputEmail.data
        _password = form.inputPassword.data

        user = db.session.query(models.User).filter_by(email=_email).first()
        if user is None:
            flash('Wrong email address or password!')
        else:
            if user.check_password(_password):
                session['user'] = user.user_id
                return redirect('/userHome')
            else:
                flash('Wrong email address or password!')

    return render_template('signin.html', form=form)


@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    form = SignUpForm()

    if form.validate_on_submit():
        print("Validate on submit")
        _fname = form.inputFirstName.data
        _lname = form.inputLastName.data
        _email = form.inputEmail.data
        _password = form.inputPassword.data

        if (db.session.query(models.User).filter_by(email=_email).count() == 0):
            user = models.User(first_name=_fname, last_name=_lname, email=_email)
            user.set_password(_password)
            db.session.add(user)
            db.session.commit()
            return render_template('signUpSuccess.html', user=user)
        else:
            flash('Email {} is already exsits!'.format(_email))
            return render_template('signup.html', form=form)

    print("Not validate on submit")
    return render_template('signup.html', form=form)

@app.route('/userHome', methods=['GET', 'POST'])
def userHome():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        return render_template('userhome.html', user=user)
    else:
        return redirect('/')

@app.route('/LogOut')
def LogOut():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect('/userHome')

@app.route('/newProject', methods=['GET','POST'])
def newProject():
	_user_id = session.get('user')
	form = ProjectForm()

	if _user_id:
		user = db.session.query(models.User).filter_by(user_id=_user_id).first()

		if form.validate_on_submit():
			_name = form.inputName.data
			_description = form.inputDescription.data
			_deadline = form.inputDeadline.data

			_project_id = request.form['hiddenProjectId']

			if (_project_id == "0"):
				project = models.Project(project_name=_name, description=_description, deadline=_deadline, status_id='1', user=user)
				db.session.add(project)

			else:
				project = db.session.query(models.Project).filter_by(project_id=_project_id).first()
				project.project_name = _name
				project.description  = _description
				project.deadline = _deadline
			db.session.commit()
			return redirect('/userHome')

		return render_template('/newproject.html', form=form, user=user)

	return redirect('/')


@app.route('/complete', methods=['GET', 'POST'])
def complete():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        project_id = request.form.get("hiddenProjectId", False)
    print(user)
    print(project_id)

    print(project_id)
    if project_id:
        project = db.session.query(models.Project).filter_by(project_id=project_id).first()
        project.status_id = "3"
        db.session.commit()
    return render_template('userhome.html', user=user)

@app.route('/deleteProject', methods=['GET', 'POST'])
def deleteProject():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        project_id = request.form.get("hiddenProjectId", False)
    print(user)

    # task_id = record_id
    if project_id:
        project = db.session.query(models.Project).filter_by(project_id=project_id).first()
        db.session.delete(project)
        db.session.commit()

    return render_template('userhome.html', user=user)

@app.route('/editProject', methods=['GET', 'POST'])
def editProject():
    _user_id = session.get('user')
    form = ProjectForm()

    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        project_id = request.form.get("hiddenProjectId", False)
        print(user)
        # task_id = record_id
        print(project_id)
        if project_id:
            project = db.session.query(models.Project).filter_by(project_id=project_id).first()
            form.inputName.default = project.project_name
            form.inputDescription.default = project.description
            form.inputDeadline.default = project.deadline
            form.process()
            return render_template('newproject.html', form=form, user=user, project=project)

    return redirect('/')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port="8080", debug=True)
