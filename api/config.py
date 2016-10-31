import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:pass@localhost/capstone_icu'
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SQLALCHEMY_TRACK_MODIFICATIONS = False

IMAGE_DIRECTORY = "/database/images/"

# Todo: figure out what pi sends
ALLOWED_EXTENSIONS = ["jpg", "jpeg", "gif", "png"]

# Maximum size for files (to make sure images aren't too large)
# MAX_CONTENT_LENGTH = 16 * 1024 * 1024
