from dotenv import load_dotenv

from views import app
from views.mercadopago_views import MercadoPagoViews


def main():
    load_dotenv()
    mercadopago_views = MercadoPagoViews()

    app.add_url_rule("/create-order", view_func=mercadopago_views.create_order)
    app.add_url_rule(
        "/notification", view_func=mercadopago_views.notification, methods=["POST"]
    )
    app.add_url_rule("/payment/<payment_id>", view_func=mercadopago_views.get_payment)

    app.add_url_rule("/success", view_func=mercadopago_views.success)
    app.add_url_rule("/pending", view_func=mercadopago_views.pending)
    app.add_url_rule("/failure", view_func=mercadopago_views.failure)

    server = app.server


if __name__ == "__main__":
    main()
