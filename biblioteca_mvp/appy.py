from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
from datetime import date, timedelta
from functools import wraps

app = Flask(__name__)


app.secret_key = "biblioteca_secreta_cambiar_en_produccion"
