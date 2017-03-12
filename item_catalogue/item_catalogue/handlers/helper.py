from flask import session as login_session

def is_signed_in():
    if "username" not in login_session:
        return False
    return True

def is_data_changed(
        new_title, new_description, new_item_slug, new_category_id, old_item):
    if not (new_title == old_item.name):
        return True
    if not (new_item_slug == old_item.slug):
        return True
    if not (new_description == old_item.description):
        return True
    if not (new_category_id == old_item.category_id):
        return True
    return False

def is_unique(count):
    if count is not 0:
        return False
    else:
        return True

def generate_slug(title):
    lowercase_title = title.lower()
    slug = "_".join(lowercase_title.split())

    return slug