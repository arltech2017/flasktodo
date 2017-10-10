from os import path
global src_path
src_path = path.dirname(path.realpath(__file__))
from .todo import app
