from flask_login import UserMixin
from setup import db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash

# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = "user_table"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(), unique=False, nullable=False)

    def __init__(self, username, email, password) -> None:
        super().__init__()
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def __repr__(self) -> str:
        print(f"User({self.username}, useremail@mail.com, ########)")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
