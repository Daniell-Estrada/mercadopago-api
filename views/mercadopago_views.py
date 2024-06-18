from typing import Optional, Tuple

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

    @staticmethod
    def layout_response(response) -> Tuple[Response, int]:
        return jsonify(response["response"]), int(response["status"])

    def create_preference(self):
        try:
            preference_object = self.validate.validate(request.json)

            result = self.preference.create(
                {
                    **preference_object,
                    "auto_return": "approved",
                    "notification_url": f"{self.HOST}/api/notification",
                }
            )
            if result["status"] == 201:
                return self.layout_response(result)

            return jsonify({"error": result["response"]}), 400

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def notification(self) -> Tuple[Response, int]:
        payment = request.args

        try:
            if payment.get("type") == "payment":
                return self.get_payment(payment["data.id"])

            return jsonify({"error": "Invalid payment."}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def get_payment(self, payment_id: Optional[str] = None) -> Tuple[Response, int]:
        response = self.payment.get(payment_id)
        return self.layout_response(response)

    def get_preference(
        self, preference_id: Optional[str] = None
    ) -> Tuple[Response, int]:
        response = self.preference.get(preference_id)
        return self.layout_response(response)
