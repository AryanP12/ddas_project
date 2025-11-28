# config.py

import os

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# SQLAlchemy Database URI
# Format: postgresql://username:password@host:port/database_name
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:YOUR_DB_PASSWORD@localhost'

# Disable modification tracking to save resources
SQLALCHEMY_TRACK_MODIFICATIONS = False