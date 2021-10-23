news_feed_input_schema = {
    'type': 'object',
    'required': ['user_id', 'post'],
    'properties': {
        'user_id': {'type': 'string'},
        'post': {
            'type': 'array',
            'contains': {
                'type': 'object',
                'required': ['language_iso', 'title', 'body'],
                'properties': {
                    'language_iso': {'type': 'string', 'minLength': 2, 'maxLength': 2},
                    'title': {'type': 'string'},
                    'body': {'type': 'string'},
                },
            },
            'minContains': 1,
        },
    },
}

companies_add_company_input_schema = {
    'type': 'object',
    'required': ['content_languages_iso', 'name'],
    'properties': {
        'addresses': {
            'type': 'array',
            'minContains': 1,
            'contains': {
                'type': 'object',
                'required': ['city', 'country_iso', 'county', 'street_address', 'zip_code'],
                'properties': {
                    'address_type': {'type': 'string'},
                    'addressee': {'type': 'string'},
                    'city': {'type': 'string'},
                    'co_address': {'type': 'string'},
                    'country_iso': {'type': 'string', 'minLength': 2, 'maxLength': 2},
                    'county': {'type': 'string'},
                    'street_address': {'type': 'string'},
                    'zip_code': {'type': 'string'},
                },
            },
        },
        'company_types': {
            'type': 'array',
            'contains': {'type': 'string', 'minLength': 2, 'maxLength': 2},
        },
        'content_languages_iso': {
            'type': 'array',
            'minContains': 1,
            'contains': {'type': 'string'},
        },
        'name': {
            'type': 'array',
            'minContains': 1,
            'contains': {
                'type': 'object',
                'required': ['language_iso', 'name'],
                'properties': {
                    'language_iso': {'type': 'string', 'minLength': 2, 'maxLength': 2},
                    'name': {'type': 'string'},
                },
            },
        },
    },
}

addresses_add_address_schema = {
    'type': 'object',
    'required': ['city', 'country_iso', 'county', 'street_address', 'zip_code'],
    'properties': {
        'address_type': {'type': 'string'},
        'addressee': {'type': 'string'},
        'city': {'type': 'string'},
        'co_address': {'type': 'string'},
        'country_iso': {'type': 'string', 'minLength': 2, 'maxLength': 2},
        'county': {'type': 'string'},
        'street_address': {'type': 'string'},
        'zip_code': {'type': 'string'},
    },
}
