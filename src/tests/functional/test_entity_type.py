def test_entity_type_list(client, test_data):
    response = client.get("/entity-type/")
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "name": "product",
                "description": "",
                "uuid": "e3105dbb-937e-43a3-bcc0-5f6500cb1f10",
                "fields": {
                    "product_number": {
                        "uuid": "f6d7bdd9-f426-4515-b51a-5daad906e131",
                        "name": "product_number",
                        "data_type": "string",
                        "input_type": "text",
                        "default": "",
                        "description": "",
                        "choices": None,
                        "required": False,
                    }
                },
                "links": {
                    "b8e6df9f-2b75-4f96-b955-70a216d170e5": {
                        "direction": "bi_directional",
                        "entity_type": "organisation",
                    }
                },
                "metadata": {},
            },
            {
                "name": "user",
                "description": "",
                "uuid": "99ac59e7-74a7-4900-a482-d93441b3edd1",
                "fields": {
                    "name": {
                        "uuid": "8742424e-46de-45e4-8d98-4a4d3ddb66b5",
                        "name": "name",
                        "data_type": "string",
                        "input_type": "text",
                        "default": "",
                        "description": "",
                        "choices": None,
                        "required": False,
                    }
                },
                "links": {
                    "b8e6df9f-2b75-4f96-b955-70a216d170e5": {
                        "direction": "bi_directional",
                        "entity_type": "organisation",
                    }
                },
                "metadata": {},
            },
            {
                "name": "organisation",
                "description": "",
                "uuid": "b8e6df9f-2b75-4f96-b955-70a216d170e5",
                "fields": {
                    "name": {
                        "uuid": "2bb37c7d-3aa2-4d0d-ad9a-6b15149c1605",
                        "name": "name",
                        "data_type": "string",
                        "input_type": "text",
                        "default": "",
                        "description": "",
                        "choices": None,
                        "required": False,
                    }
                },
                "links": {},
                "metadata": {},
            },
        ],
        "total": 3,
        "page": 1,
        "size": 50,
    }


def test_entity_type_create(client, test_data, test_user):
    response = client.post(
        "/entity-type/",
        json={
            "name": "supplier",
            "description": "",
            "fields": {
                "supplier_number": {
                    "uuid": "be06dc7e-6071-4150-b714-2e4f4bf956e3",
                    "name": "supplier_number",
                    "input_type": "text",
                    "data_type": "string",
                }
            },
        },
    )
    assert response.status_code == 200
    assert "supplier" == response.json()["name"]
    assert "supplier_number" in response.json()["fields"]

    response = client.get("/entity-type/")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 4


def test_entity_type_update(client, test_data, test_user):
    entity_uuid = test_data["productEntityType"]["uuid"]
    response = client.patch(
        f"/entity-type/{entity_uuid}/",
        json={
            "name": "product_2",
            "description": "",
            "uuid": entity_uuid,
            "fields": {
                "product_number_2": {
                    "name": "product_number_2",
                    "uuid": "a66adada-4ec0-4ddd-9d67-769e5b68c6c8",
                    "input_type": "text",
                    "data_type": "string",
                }
            },
            "links": {},
            "metadata": {},
        },
    )
    assert response.status_code == 200, response.json()
    assert "product_2" == response.json()["name"]
    assert "product_number_2" in response.json()["fields"]


def test_entity_delete(client, test_data, test_user):
    entity_uuid = test_data["productEntityType"]["uuid"]
    response = client.delete(f"/entity-type/{entity_uuid}/")
    assert response.status_code == 201, response.json()

    response = client.get("/entity-type/")
    assert response.status_code == 200, response.json()
    assert len(response.json()["items"]) == 2
