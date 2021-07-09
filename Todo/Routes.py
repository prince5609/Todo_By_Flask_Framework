from Todo import app, db
from flask import render_template, request, redirect, url_for, flash
from Todo.Forms import AddTodoForm, RegisterForm, LoginForm, UpdateForm
from Todo.Models import User, Todos
from flask_login import login_user, login_required, logout_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template("Home.html")


@app.route('/about')
def about_page():
    return render_template("About.html")


@app.route('/todo', methods=["GET", "POST"])
@login_required
def todo_page():
    form = AddTodoForm()
    if request.method == "POST":
        todo = Todos(title=form.title.data, description=form.description.data)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("todo_page"))
    if request.method == "GET":
        todos = Todos.query.filter_by(client=None)
        return render_template("Todo.html", form=form, todos=todos)


@app.route('/register', methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data
                              )
        db.session.add(user_to_create)
        db.session.commit()
        flash(f"Congratulations {user_to_create.username} You Have created Your Account Successfully",
              category='Success')
        return redirect(url_for("todo_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template("Register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email_address=form.email_address.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Welcome {attempted_user.username}", category="success")
            return redirect(url_for("todo_page"))
        else:
            flash("Email_address and Password Don't Match, Please Try Again", category="danger")
    return render_template("Login.html", form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You Have Been logged Out Successfully", category="info")
    return redirect(url_for("home_page"))


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todos.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo_page"))


@app.route('/update/<int:sno>', methods=["GET", "POST"])
def update(sno):
    form = UpdateForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        todo = Todos.query.filter_by(sno=sno).first()
        todo.title = title
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("todo_page"))
    todo = Todos.query.filter_by(sno=sno).first()
    return render_template("Update.html", todo=todo, form=form)
