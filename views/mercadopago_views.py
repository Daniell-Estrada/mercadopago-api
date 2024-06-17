from typing import Any, Optional

from mercadopago import SDK

from . import *


class MercadoPagoViews:
    def __init__(self) -> None:
        self.HOST = getenv("HOST")
        MP_ACCESS_TOKEN = getenv("MP_ACCESS_TOKEN")

        self.client = SDK(MP_ACCESS_TOKEN)
        self.preference = self.client.preference()
        self.payment = self.client.payment()

        self.validate = PreferenceValidator()

    def create_order(self):
        try:
            preference_object = self.validate.validate(request.json)

            result = self.preference.create(
                {
                    **preference_object,
                    "auto_return": "approved",
                    "notification_url": f"{self.HOST}/notification",
                    "back_urls": {
                        "success": f"{self.HOST}/success",
                        "pending": f"{self.HOST}/pending",
                        "failure": f"{self.HOST}/failure",
                    },
                }
            )
            if result["status"] != 201:
                return jsonify({"error": result["response"]}), 400
            
            print(result["response"]["init_point"])
            return redirect(result["response"]["init_point"], code=302)

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def notification(self):
        payment = request.args

        try:
            if payment.get("type") == "payment":
                payment_info = self.get_payment(payment.get("data_id"))
                print(payment_info)
                return jsonify(payment_info)

            return jsonify({"error": "Invalid payment"})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

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
