def test_entity_type_list(client, test_data):
    response = client.get("/entity-type/")
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "name": "product",
                "uuid": "e3105dbb-937e-43a3-bcc0-5f6500cb1f10",
                "fields": {
                    "product_number": {
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
            },
            {
                "name": "user",
                "uuid": "99ac59e7-74a7-4900-a482-d93441b3edd1",
                "fields": {
                    "name": {
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
            },
            {
                "name": "organisation",
                "uuid": "b8e6df9f-2b75-4f96-b955-70a216d170e5",
                "fields": {
                    "name": {
                        "data_type": "string",
                        "input_type": "text",
                        "default": "",
                        "description": "",
                        "choices": None,
                        "required": False,
                    }
                },
                "links": {},
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
            "fields": {
                "supplier_number": {"input_type": "text", "data_type": "string"}
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
            "uuid": entity_uuid,
            "fields": {
                "product_number_2": {"input_type": "text", "data_type": "string"}
            },
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
