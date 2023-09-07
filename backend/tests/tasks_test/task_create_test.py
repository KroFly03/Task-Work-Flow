import json
from types import NoneType


class TestCreateTaskView:
    url = 'tasks'
    initial_data = {
        'name': 'test',
        'description': 'test',
        'employee_id': 1
    }

    def test_correct_return_data_keys(self, client):
        response = client.post(self.url, data=json.dumps(self.initial_data))
        print(response.json())
        assert list(response.json().keys()) == ['id', 'name', 'description', 'status', 'employee', 'parent', 'deadline']
        assert list(response.json().get('employee').keys()) == ['name', 'job', 'id']

    def test_correct_return_status_code(self, client):
        response = client.post(self.url, data=json.dumps(self.initial_data))

        assert response.status_code == 200

    def test_correct_return_data_type(self, client):
        response = client.post(self.url, data=json.dumps(self.initial_data))

        assert [type(value) for value in response.json().values()] == [int, str, str, list, dict, NoneType, NoneType]
        assert [type(value) for value in response.json().get('employee').values()] == [str, str, int]
