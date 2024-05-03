from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app.projects.project_1 import project_1_bp
from app.setup import app, db
from app.setup.forms.login import LoginForm
from app.setup.forms.register import RegisterForm
from app.setup.models.user import User


@app.route("/")
def home():
    return "hello world"


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit() and request.method == "POST":
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        flash("Thanks for registering!")
        return redirect(url_for("login"))
    active_tab = "home"
    return render_template("register.html", form=form, active_tab=active_tab)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit() and request.method == "POST":
        user = User.query.filter_by(form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("Logged in successfully.")
            next = request.args.get("next")
            if next is None or not next[0] == "/":
                next = url_for("home")
            return redirect(next)

    active_tab = "home"
    return render_template("login.html", form=form, active_tab=active_tab)


@app.route("/skills")
@login_required
def skills():
    active_tab = "skills"
    return render_template("skills.html", active_tab=active_tab)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You Logged Out!")
    return redirect(url_for("home"))


@app.route("/projects")
def projects():
    active_tab = "projects"
    projects_data = [
        {
            "name": "Project 1",
            "description": "A description of project 1.",
            "category": "Category 1",
            "skills_used": "Skill A, Skill B",
        },
        {
            "name": "Project 2",
            "description": "A description of project 2.",
            "category": "Category 2",
            "skills_used": "Skill C, Skill D",
        },
        # Add more projects as needed
    ]
    return render_template(
        "projects.html", projects=projects_data, active_tab=active_tab
    )


@app.route("/aboutme")
def aboutme():
    active_tab = "aboutme"
    return render_template("aboutme.html", active_tab=active_tab)


app.register_blueprint(project_1_bp)

if __name__ == "__main__":
    app.run(host="o.0.0.0", port=5000)
