from dotenv import load_dotenv
from gevent.pywsgi import WSGIServer

from views import app
from views.mercadopago_views import MercadoPagoViews


def create_app():
    load_dotenv()

    mercadopago_views = MercadoPagoViews()

    app.add_url_rule(
        "/preference",
        view_func=mercadopago_views.create_preference,
        methods=["POST"],
    )

    app.add_url_rule(
        "/notification", view_func=mercadopago_views.notification, methods=["POST"]
    )
    app.add_url_rule(
        "/payment/<string:payment_id>", view_func=mercadopago_views.get_payment
    )

    app.add_url_rule(
        "/preference/<string:preference_id>", view_func=mercadopago_views.get_preference
    )

    app.add_url_rule("/success", view_func=mercadopago_views.success)
    app.add_url_rule("/pending", view_func=mercadopago_views.pending)
    app.add_url_rule("/failure", view_func=mercadopago_views.failure)

    return WSGIServer(("", 8000), app)
    # return app


if __name__ == "__main__":
    # create_app().run(port=5000, debug=True)  # This is for development
    create_app().serve_forever()  # This is for production
