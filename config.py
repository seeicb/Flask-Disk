import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'H7XyGqdqghcoCH7T4cf!'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WTF_CSRF_SECRET_KEY = 'H7XyGqdqghcoCH7T4cf!'
    WTF_CSRF_CHECK_DEFAULT = True
	# 最大上传限制，默认1024M
    MAX_CONTENT_LENGTH = 1024 * 1024 * 1024
	# Cookie 过期时间
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    FONT=basedir+'/app/static/font/Arial.ttf'
	# HDFS回收站文件路径
    HDFS_TRASH = '/user/username/.Trash/Current/'
	# HDFS namenode
    HDFS_IP = "http://127.0.0.1:50070"
    SESSION_COOKIE_HTTPONLY=True

    @staticmethod
    def init__app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    BASE_HOST='http://127.0.0.1:5000/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'web_db.sqlite')



class TestingConfig(Config):
    pass


class Production(Config):
    DEBUG = False
    BASE_HOST = 'http://127.0.0.1:5000/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'web_db.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': Production,
    'default': DevelopmentConfig
}
