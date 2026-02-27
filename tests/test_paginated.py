from typing import Any

from rocketchat_API.APISections.base import paginated


class MockAPI:
    def __init__(self, total_items: int) -> None:
        self.total_items = total_items
        self.call_count = 0

    @paginated("items")
    def get_items(self, **kwargs: Any) -> dict[str, Any]:
        self.call_count += 1
        offset = kwargs.get("offset", 0)
        count = kwargs.get("count", 50)
        start = offset
        end = min(offset + count, self.total_items)
        items = [{"id": i, "name": f"item_{i}"} for i in range(start, end)]
        return {"items": items, "success": True}


class TestPaginatedDecorator:
    def test_basic_pagination(self):
        api = MockAPI(total_items=150)
        result = list(api.get_items(count=50))

        assert len(result) == 150
        assert api.call_count == 4

    def test_max_count_less_than_total(self):
        api = MockAPI(total_items=150)
        result: list[dict[str, Any]] = list(api.get_items(max_count=100))

        assert len(result) == 100
        assert result[0]["id"] == 0
        assert result[99]["id"] == 99

    def test_max_count_greater_than_total(self):
        api = MockAPI(total_items=50)
        result = list(api.get_items(max_count=100))

        assert len(result) == 50

    def test_max_count_exact_page_boundary(self):
        api = MockAPI(total_items=150)
        result = list(api.get_items(count=50, max_count=100))

        assert len(result) == 100
        assert api.call_count == 2

    def test_max_count_mid_page(self):
        api = MockAPI(total_items=150)
        result = list(api.get_items(count=50, max_count=75))

        assert len(result) == 75
        assert api.call_count == 2

    def test_max_count_one(self):
        api = MockAPI(total_items=150)
        result: list[dict[str, Any]] = list(api.get_items(max_count=1))

        assert len(result) == 1
        assert result[0]["id"] == 0
        assert api.call_count == 1

    def test_max_count_zero_returns_empty(self):
        api = MockAPI(total_items=150)
        result = list(api.get_items(max_count=0))

        assert len(result) == 0

    def test_max_count_none_returns_all(self):
        api = MockAPI(total_items=75)
        result = list(api.get_items(count=50))

        assert len(result) == 75
        assert api.call_count == 2

    def test_offset_with_max_count(self):
        api = MockAPI(total_items=150)
        result: list[dict[str, Any]] = list(api.get_items(offset=50, max_count=50))

        assert len(result) == 50
        assert result[0]["id"] == 50
        assert result[49]["id"] == 99

    def test_custom_count_with_max_count(self):
        api = MockAPI(total_items=100)
        result = list(api.get_items(count=10, max_count=25))

        assert len(result) == 25
        assert api.call_count == 3

    def test_generator_behavior(self):
        api = MockAPI(total_items=100)
        gen = api.get_items(max_count=10)

        assert hasattr(gen, "__iter__")
        assert hasattr(gen, "__next__")

        items = []
        for item in gen:
            items.append(item)

        assert len(items) == 10

    def test_empty_response(self):
        api = MockAPI(total_items=0)
        result = list(api.get_items())

        assert len(result) == 0
        assert api.call_count == 1

    def test_empty_response_with_max_count(self):
        api = MockAPI(total_items=0)
        result = list(api.get_items(max_count=100))

        assert len(result) == 0
        assert api.call_count == 1
