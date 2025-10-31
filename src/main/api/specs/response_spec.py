from http import HTTPStatus
from requests import Response

class ResponseSpec:
    @staticmethod
    def request_return_ok():
        def check(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text
        return check

    @staticmethod
    def entity_was_created():
        def check(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text
        return check
    
    @staticmethod
    def request_return_bad_request (error_key: str, error_value: str):
        def check(response: Response):
           assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
           assert error_value in response.json().get(error_key)  
        return check
    
    @staticmethod
    def entity_was_deleted():
        def check(response: Response):
            assert response.status_code in (HTTPStatus.NO_CONTENT, HTTPStatus.OK), response.text
        return check    


    @staticmethod
    def request_return_bad_request(error_key: str, error_value: str):
        def check(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
            try:
                payload = response.json()
            except ValueError:
                assert error_value in response.text
                return

            field_value = payload.get(error_key, "")
            if isinstance(field_value, (list, tuple, set)):
                field_value = " ".join(map(str, field_value))
            assert error_value in str(field_value)

        return check
