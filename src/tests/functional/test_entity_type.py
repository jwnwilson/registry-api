def test_entity_type_list(client, test_data):
    response = client.get("/entity-type/")
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "name": "product",
                "uuid": "e3105dbb-937e-43a3-bcc0-5f6500cb1f10",
                "owner": "01f2612b-e277-4ed5-91a3-254fc8c09325",
                "organisation": None,
                "fields": {
                    "product_number": {
                        "type": "string", 
                        "default": None, 
                        "description": "", 
                        "choices": None, 
                        "required": True
                    }
                }
            }
        ], 
        "total": 1, 
        "page": 1, 
        "size": 50
    }


def test_entity_type_create(client, test_data, test_user):
    response = client.post("/entity-type/", json={
            "name": "supplier",
            "owner": test_user.user_id,
            "organisation": test_user.organisation_id,
            "fields": {
                "supplier_number": {
                    "type": "string" 
                }
            }
        }
    )
    assert response.status_code == 200
    assert "supplier" == response.json()["name"]
    assert "supplier_number" in response.json()["fields"]

    response = client.get("/entity-type/")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 2


def test_entity_type_update(client, test_data, test_user):
    entity_uuid = test_data["entityType"]["uuid"]
    response = client.patch(f"/entity-type/{entity_uuid}/", json={
            "name": "product_2",
            "uuid": entity_uuid,
            "owner": test_user.user_id,
            "organisation": test_user.organisation_id,
            "fields": {
                "product_number_2": {
                    "input_type": "text",
                    "data_type": "string"
                }
            }
        }
    )
    assert response.status_code == 200, response.json()
    assert "product_2" == response.json()["name"]
    assert "product_number_2" in response.json()["fields"]


def test_entity_delete(client, test_data, test_user):
    entity_uuid = test_data["entityType"]["uuid"]
    response = client.delete(f"/entity-type/{entity_uuid}/")
    assert response.status_code == 201, response.json()

    response = client.get("/entity-type/")
    assert response.status_code == 200, response.json()
    assert len(response.json()["items"]) == 0
