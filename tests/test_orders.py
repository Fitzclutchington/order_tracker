import pytest
from fastapi import status


@pytest.mark.xfail(
    reason="API returns HTML, not json. Will update when I swtich to Javascript instead of Jinja"
)
def test_read_all_orders(test_order, test_client):
    response = test_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "name": test_order.name,
            "status": test_order.status,
            "created_at": test_order.created_at,
            "id": test_order.id,
        }
    ]
