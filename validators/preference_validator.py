from typing import Any, Optional


class PreferenceValidator:
    def __init__(self) -> None:
        self.items = ["id", "title", "description", "quantity", "unit_price"]
        self.payer = ["name", "email"]

    def validate(self, preference: Any) -> dict:
        if preference.get("items") and preference.get("payer"):
            items = preference["items"]
            payer = preference["payer"]

            if self.validate_items(items) and self.validate_payer(payer):
                return preference

        raise ValueError("Invalid preference")

    def validate_items(self, items: dict) -> Optional[bool]:
        def validate_item(keys: list[str]) -> bool:
            for item in items:
                if not all([k in item for k in self.items]):
                    return False

                if any([isinstance(item[k], str) for k in keys]):
                    return False

            return True

        if validate_item(keys=["quantity", "unit_price"]):
            return True

        raise ValueError("Invalid items")

    def validate_payer(self, payer: dict) -> bool:
        if all([key in self.payer for key in payer]):
            return True
        raise ValueError("Invalid payer")
