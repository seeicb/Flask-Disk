from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class UserTable(UserMixin, db.Model):
    __tablename__ = 'UserTable'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_lock = db.Column(db.Boolean, default=False)
    # 其它信息
    real_name = db.Column(db.String(100))
    phone_number = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    address = db.Column(db.String(100))
    about_me = db.Column(db.Text())

    @staticmethod
    def insert_admin():
        username = "admin"
        email = "admin@admin.com"
        password = "password"
        user = UserTable(username=username, email=email, password=password, is_admin=True)
        db.session.add(user)
        db.session.commit()

    def get_id(self):
        return self.user_id

    def get_is_admin(self):
        if self.is_admin:
            return True
        else:
            return False

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return UserTable.query.get(int(user_id))


class FileTable(db.Model):
    __tablename__ = 'FileTable'

    file_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(100), nullable=False)
    file_ext = db.Column(db.String(100))
    file_size = db.Column(db.Integer, nullable=False)
    file_mime = db.Column(db.String(100))
    file_category = db.Column(db.String(100))
    create_time = db.Column(db.DateTime, nullable=False)
    is_share = db.Column(db.Boolean, default=False)
    is_recycle = db.Column(db.Boolean, default=False)
    hdfs_path = db.Column(db.String(50), nullable=False)
    hdfs_filename = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)


class ShareTable(db.Model):
    __tablename__ = 'ShareTable'

    share_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_id = db.Column(db.Integer, nullable=False)
    share_url = db.Column(db.String(100), nullable=False)
    share_pass = db.Column(db.String(20), default='')


class RecycleTable(db.Model):
    __tablename__ = 'RecycleTable'

    recycle_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_id = db.Column(db.Integer, nullable=False)
    recycle_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
