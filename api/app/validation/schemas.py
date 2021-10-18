news_feed_input_schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'},
        'post': {
            'type': 'array',
            'contains': {
                'type': 'object',
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
