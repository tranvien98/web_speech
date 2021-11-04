from flask import Blueprint
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from model import *

view_edit = Blueprint('view_edit', __name__)
