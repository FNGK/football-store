def test_health(client):
    res = client.get("/health")
    assert res.status_code in (200, 503)
    assert "checks" in res.json()


def test_login_and_me(client, auth_headers):
    res = client.get("/v1/auth/me", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == "test-admin@example.com"
    assert "tenant_id" in data


def test_unauthorized_without_token(client):
    res = client.get("/v1/auth/me")
    assert res.status_code == 401
