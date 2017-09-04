# -*- coding:utf-8 -*-

import os

f = open('config.txt', 'r')
content = f.readlines()
f.close()


init_config = {}
for each in content:
    config_key, config_value = each.split(',')
    init_config[config_key] = config_value[:-1]


class Config:
    SECRET_KEY = os.environ.get('SECREC_KEY') or init_config['SECRET_KEY']
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')
    FLASK_ADMIN_EMAIL = os.environ.get('FLASK_ADMIN_EMAIL') or init_config['FLASK_ADMIN_EMAIL']
    MAIL_USE_TLS = True
    FLASKY_MAIL_SUBJECT_PREFIX = os.environ.get('FLASKY_MAIL_SUBJECT_PREFIX') or init_config['FLASKY_MAIL_SUBJECT_PREFIX']
    FLASKY_MAIL_SENDER = os.environ.get('FLASKY_MAIL_SENDER') or init_config['FLASKY_MAIL_SENDER']
    UPLOADED_AVATARS_DEST = os.environ.get('UPLOADED_AVATARS_DEST') or init_config['UPLOADED_AVATARS_DEST']

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or init_config['SQLALCHEMY_DATABASE_URI_dev']


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
