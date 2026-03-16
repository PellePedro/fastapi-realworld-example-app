from slugify import slugify


def get_slug_for_category(name: str) -> str:
    return slugify(name)
