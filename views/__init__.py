from os import getenv

from flask import (Blueprint, Flask, Request, Response, jsonify, redirect,
                   request)
from flask_cors import CORS

from validators.preference_validator import PreferenceValidator

app = Flask(__name__)
prefix = Blueprint("prefix", __name__)


__flask__ = [
    "app",
    "prefix",
    "CORS",
    "Request",
    "Response",
    "jsonify",
    "request",
    "redirect",
]
__validators__ = ["PreferenceValidator"]
__other__ = ["getenv"]


__all__ = __flask__ + __validators__ + __other__

from . import mercadopago_views
