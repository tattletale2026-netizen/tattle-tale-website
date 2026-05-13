import sys
import os

# Set up the path to the application
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app
# GoDaddy/Passenger expects the callable to be named 'application'
from app import app as application
