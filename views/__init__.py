from os import getenv

from flask import Flask, Request, Response, jsonify, redirect, request

from validators.preference_validator import PreferenceValidator

app = Flask(__name__)


__flask__ = ["app", "Request", "Response", "jsonify", "request", "redirect"]
__validators__ = ["PreferenceValidator"]
__other__ = ["getenv"]


__all__ = __flask__ + __validators__ + __other__

from . import mercadopago_views
