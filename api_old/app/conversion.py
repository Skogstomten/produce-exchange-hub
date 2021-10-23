def post_object_to_address_dict(post_obj: dict) -> dict:
    return {
        'address_type': post_obj.get('address_type', None),
        'addressee': post_obj.get('addressee', None),
        'co_address': post_obj.get('co_address', None),
        'country_iso': post_obj.get('country_iso'),
        'county': post_obj.get('county'),
        'street_address': post_obj.get('street_address'),
        'zip_code': post_obj.get('zip_code'),
    }
