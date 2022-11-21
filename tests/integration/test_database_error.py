import json
import server
from tests.mocked_json import MockedJson


def raise_json_decode(filename):
    raise json.JSONDecodeError(doc=filename, msg='prout', pos=0)


class TestJsonFail:

    def test_raise(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        response = client.post("/login", data={"email": "test@mail.com"}, follow_redirects=True)
        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text

        monkeypatch.setattr('server.load_json', raise_json_decode)
        monkeypatch.setattr('server.save_json', raise_json_decode)

        # Go to book
        response = client.get('/showClubs', follow_redirects=True)

        assert response.status_code == 200
        assert "Database access failed" in response.text
