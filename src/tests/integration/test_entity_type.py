def test_entity_type(client, test_data):
    response = client.get("/entity-type/")
    assert response.status_code == 200
    assert response.json() == {
        'items': [
            {
                'name': 'product',
                'uuid': 'e3105dbb-937e-43a3-bcc0-5f6500cb1f10',
                'owner': '01f2612b-e277-4ed5-91a3-254fc8c09325',
                'organisation': None,
                'fields': {
                    'product_number': {
                        'type': 'string', 
                        'default': None, 
                        'description': None, 
                        'choices': None, 
                        'required': True
                    }
                }
            }
        ], 
        'total': 1, 
        'page': 1, 
        'size': 50
    }
