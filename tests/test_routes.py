import pytest


status_code_cases = [
    ("/report/", 200),
    ("/report/drivers/", 200),
    ("/report/drivers/?driver_id=SVF", 200),
    ("/report/drivers/?order=desc/", 200),
    ("/report/drivers/?driver_id=SVFS/", 404),
    ("/report/driver/", 404),
    ("/reports/", 404),
    ("/", 404)
]


@pytest.mark.parametrize('route, result', (status_code_cases))
def test_status(client, route, result):
    response = client.get(route)
    assert response.status_code == result
