from typing import Any, Optional

from mercadopago import SDK

from . import *


class MercadoPagoViews:
    def __init__(self) -> None:
        MP_ACCESS_TOKEN = getenv("MP_ACCESS_TOKEN")

        self.client = SDK(MP_ACCESS_TOKEN)
        self.preference = self.client.preference()
        self.payment = self.client.payment()

    def create_order(self):
        # preference_object = request.json

        preference_object = {
            "items": [
                {
                    "id": "456",
                    "description": "Laptop Dell Inspiron 15 3000",
                    "picture_url": "http://product1.image.png",
                    "quantity": 2,
                    "title": "Item 1",
                    "currency_id": "COP",
                    "unit_price": 100000,
                }
            ],
            "auto_return": "approved",
            "notification_url": "/notification",
            "back_urls": {
                "success": "/success",
                "pending": "/pending",
                "failure": "/failure",
            },
        }

        try:
            result = self.preference.create(preference_object)
            print(result["response"]["init_point"])

            return redirect(result["response"]["init_point"], code=302)

        except Exception as e:
            return jsonify({"error": str(e)})

    def notification(self):
        payment = request.args

        try:
            if payment.get("type") == "payment":
                payment_info = self.get_payment(payment.get("data_id"))
                print(payment_info)
                return jsonify(payment_info)

            return jsonify({"error": "Invalid payment"})
        except Exception as e:
            return jsonify({"error": str(e)})

    def get_payment(self, payment_id: Optional[str] = None) -> dict[str, Any]:
        return self.payment.get(
            payment_id, {"access_token": self.client.request_options.access_token}
        )

    def success(self):
        return jsonify(request.args)

    def pending(self):
        return jsonify({"message": "Payment pending"})

    def failure(self):
        return jsonify({"message": "Payment failed"})
