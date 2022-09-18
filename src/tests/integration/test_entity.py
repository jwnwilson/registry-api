def test_entity(client):
    response = client.get("/entity/product")
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "name": "knife",
                "entity_type": "product",
                "uuid": "2ddc873b-dbe9-4c89-944d-75b58ae33cca",
                "owner": "01f2612b-e277-4ed5-91a3-254fc8c09325",
                "organisation": None,
                "fields": {"product_number": "12345"},
                "links": [],
            }
        ],
        "total": 1,
        "page": 1,
        "size": 50,
    }
