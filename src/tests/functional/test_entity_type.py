def test_api_root(client):
    response = client.get("/entity-type/")
    assert response.status_code == 200
    assert response.json() == {}
