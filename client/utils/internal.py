def get_category_id_by_name(name: str, data: list[dict]) -> int:
    for category in data:
        if category["name"] == name:
            return category["id"]


def get_category_name_by_id(id: int, data: list[dict]) -> str:
    for category in data:
        if category["id"] == id:
            return category["name"]
