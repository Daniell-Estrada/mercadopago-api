from os import getenv

from flask import Flask, Request, Response, jsonify, redirect, request

app = Flask(__name__)

__flask__ = ["app", "Request", "Response", "jsonify", "request", "redirect"]
__other__ = ["getenv"]

__all__ = __flask__ + __other__

from . import mercadopago_views
