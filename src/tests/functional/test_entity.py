def test_entity_list(client, test_data):
    response = client.get("/entity/product/")
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


def test_entity_create(client, test_user, test_data):
    response = client.post(
        "/entity/product/",
        json={
            "name": "spoon",
            "entity_type": "product",
            "owner": test_user.user_id,
            "organisation": test_user.organisation_id,
            "fields": {"product_number": "54321"},
            "links": [],
        },
    )
    assert response.status_code == 200
    assert "spoon" == response.json()["name"]
    assert "product" == response.json()["entity_type"]
    assert "product_number" in response.json()["fields"]


def test_entity_update(client, test_data, test_user):
    entity_uuid = test_data["entity"]["uuid"]
    response = client.patch(
        f"/entity/product/{entity_uuid}/",
        json={
            "name": "spoon2",
            "entity_type": "product",
            "owner": test_user.user_id,
            "organisation": test_user.organisation_id,
            "fields": {"product_number": "12345"},
            "links": [],
        },
    )
    assert response.status_code == 200, response.json()

    assert "spoon2" == response.json()["name"]
    assert "product" == response.json()["entity_type"]
    assert "12345" == response.json()["fields"]["product_number"]


def test_entity_delete(client, test_data, test_user):
    entity_uuid = test_data["entity"]["uuid"]
    response = client.delete(f"/entity/product/{entity_uuid}/")
    assert response.status_code == 201, response.json()

    response = client.get("/entity/product")
    assert response.status_code == 200, response.json()
    assert len(response.json()["items"]) == 0
