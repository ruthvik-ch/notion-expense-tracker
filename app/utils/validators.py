def validate_categories(data: dict, category_map: dict):
    for c in data["categories"]:
        if c not in category_map:
            raise ValueError(f"Invalid category: {c}")
