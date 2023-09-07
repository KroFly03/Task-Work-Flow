import json


class TestCreateEmployeeView:
    url = 'employees'
    initial_data = {
        'name': 'test',
        'job': 'test',
    }

    def test_correct_return_data_keys(self, client):
        response = client.post(self.url, data=json.dumps(self.initial_data))

        assert list(response.json().keys()) == ['name', 'job', 'id']

    def test_correct_return_status_code(self, client):
        response = client.post(self.url, data=json.dumps(self.initial_data))

        assert response.status_code == 200

    def test_correct_return_data_type(self, client):
        response = client.post(self.url, data=json.dumps(self.initial_data))

        assert [type(value) for value in response.json().values()] == [str, str, int]
