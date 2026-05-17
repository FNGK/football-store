def test_ingest_conversion(client, auth_headers):
    res = client.post(
        "/v1/crm/conversions",
        headers=auth_headers,
        json={
            "gclid": "test-gclid",
            "consent_ad_storage": "granted",
            "consent_analytics_storage": "denied",
            "source": "observed",
            "value_usd": 99.5,
        },
    )
    assert res.status_code == 201
    body = res.json()
    assert body["source"] == "observed"
