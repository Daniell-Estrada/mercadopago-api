from dotenv import load_dotenv
from gevent.pywsgi import WSGIServer

from views import CORS, app, prefix
from views.mercadopago_views import MercadoPagoViews


def create_app():
    load_dotenv()

    mercadopago_views = MercadoPagoViews()

    prefix.add_url_rule(
        "/preference", view_func=mercadopago_views.create_preference, methods=["POST"]
    )

    prefix.add_url_rule(
        "/notification", view_func=mercadopago_views.notification, methods=["POST"]
    )

    prefix.add_url_rule(
        "/payment/<string:payment_id>",
        view_func=mercadopago_views.get_payment,
        methods=["GET"],
    )

    prefix.add_url_rule(
        "/preference/<string:preference_id>", view_func=mercadopago_views.get_preference
    )

    app.register_blueprint(prefix, url_prefix="/api")
    CORS(app)

    return WSGIServer(("", 8000), app)
    # return app


if __name__ == "__main__":
    # create_app().run(port=5000, debug=True)  # This is for development
    create_app().serve_forever()  # This is for production
