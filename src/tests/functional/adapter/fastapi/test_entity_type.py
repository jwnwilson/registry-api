def test_entity_type_list(client, test_data):
    response = client.get("/api/v1/entity-type/")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 3


def test_entity_type_create(client, test_data, test_user):
    response = client.post(
        "/api/v1/entity-type/",
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

    response = client.get("/api/v1/entity-type/")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 4


def test_entity_type_update(client, test_data, test_user):
    entity_uuid = test_data["productEntityType"]["uuid"]
    response = client.patch(
        f"/api/v1/entity-type/{entity_uuid}/",
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
    response = client.delete(f"/api/v1/entity-type/{entity_uuid}/")
    assert response.status_code == 201, response.json()

    response = client.get("/api/v1/entity-type/")
    assert response.status_code == 200, response.json()
    assert len(response.json()["items"]) == 2
