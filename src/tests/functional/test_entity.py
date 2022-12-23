def test_entity_list(client, test_data):
    response = client.get("/entity/product/")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 2


def test_entity_create(client, test_user, test_data):
    response = client.post(
        "/entity/product/",
        json={
            "name": "spoon3",
            "entity_type": "product",
            "fields": {"product_number": "54321"},
            "links": {},
            "metadata": {},
        },
    )
    assert response.status_code == 200, response.json()
    assert "spoon3" == response.json()["name"]
    assert "product" == response.json()["entity_type"]
    assert "product_number" in response.json()["fields"]


def test_entity_update(client, test_data, test_user):
    entity_uuid = test_data["entity_1"]["uuid"]
    response = client.patch(
        f"/entity/product/{entity_uuid}/",
        json={
            "name": "spoon2",
            "description": "",
            "entity_type": "product",
            "fields": {"product_number": "12345"},
            "links": {},
            "metadata": {},
        },
    )
    assert response.status_code == 200, response.json()

    assert "spoon2" == response.json()["name"]
    assert "product" == response.json()["entity_type"]
    assert "12345" == response.json()["fields"]["product_number"]


def test_entity_delete(client, test_data, test_user):
    response = client.get("/entity/product")
    number_entities = len(response.json()["items"])

    entity_uuid = test_data["entity_1"]["uuid"]
    response = client.delete(f"/entity/product/{entity_uuid}/")
    assert response.status_code == 201, response.json()

    response = client.get("/entity/product")
    assert response.status_code == 200, response.json()
    assert len(response.json()["items"]) == (number_entities - 1)


def test_entity_set_relatioship(client, test_data, test_user):
    entity_2_uuid = test_data["entity_2"]["uuid"]
    org_uuid = test_data["organisation_1"]["uuid"]
    response = client.patch(
        f"/entity/product/{entity_2_uuid}/",
        json={
            "name": "spoon2",
            "description": "",
            "entity_type": "product",
            "fields": {"product_number": "12345"},
            "links": {
                org_uuid: {"entity_type": "organisation", "link_type": "related"},
            },
            "metadata": {},
        },
    )
    assert response.status_code == 200, response.json()

    assert len(response.json()["links"]) > 0
    assert response.json()["links"][org_uuid]["link_type"] == "related"
