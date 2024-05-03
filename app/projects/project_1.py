from flask import Blueprint, render_template

project_1_bp = Blueprint(
    "project_1", __name__, url_prefix="/projects", template_folder="templates"
)


@project_1_bp.route("/project_1")
def project_1():
    return render_template("project_1.html")


@project_1_bp.route("/project_2")
def project_2():
    return render_template("project_2.html")
