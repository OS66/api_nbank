# from http import HTTPStatus
# import requests

# from src.main.api.models.login_user_request import LoginUserRequest
# from src.main.api.models.login_user_response import LoginUserResponse
# from src.main.api.models.create_user_request import CreateUserRequest
# from src.main.api.models.create_user_response import CreateUserResponse
# from src.main.api.models.create_account_response import CreateAccountResponse
# from src.main.api.models.create_deposit_request import CreateDepositRequest
# from src.main.api.models.create_deposit_response import CreateDepositResponse
# from src.main.api.models.update_profile_request import UpdateProfileRequest
# from src.main.api.models.update_profile_response import UpdateProfileResponse
# from src.main.api.requests.requester import Requester





# class CreateAccountRequester(Requester):
#     def post(self) -> CreateAccountResponse:
#         url = f'{self.base_url}/accounts'
#         response = requests.post(url=url, headers=self.headers)
#         self.response_spec(response)
#         return CreateAccountResponse(**response.json())












# class CreateDepositRequester(Requester):
#      def post(self, create_deposit_request: CreateDepositRequest) -> CreateDepositResponse:
#         url = f'{self.base_url}/accounts/deposit'
#         response = requests.post(url=url, json=create_deposit_request.model_dump(), headers=self.headers)
#         self.response_spec(response)

#         if not response.headers.get("Content-Type", "").startswith("application/json"):
#             return response.text
#         return CreateDepositResponse(**response.json())
     









# # 


# # class CreateDepositRequester(Requester):
# #      def post(self, create_deposit_request: CreateDepositRequest) -> CreateDepositResponse:
# #         url = f'{self.base_url}/accounts/deposit'
# #         response = requests.post(url=url, json=create_deposit_request.model_dump(), headers=self.headers)
# #         self.response_spec(response)

# #         if not response.headers.get("Content-Type", "").startswith("application/json"):
# #             return response.text
# #         return CreateDepositResponse(**response.json())
     



# # class CreateDepositRequester(Requester):
# #     def post(self, create_deposit_request: CreateDepositRequest) -> CreateDepositResponse | Response:
# #         url = f"{self.base_url}/accounts/deposit"
# #         response = requests.post(url=url, json=create_deposit_request.model_dump(), headers=self.headers)
# #         self.response_spec(response)

# #         if response.status_code >= HTTPStatus.BAD_REQUEST:
# #             return response  # тест будет работать с response.json() или response.text

# #         if not response.headers.get("Content-Type", "").startswith("application/json"):
# #             return response.text

# #         return CreateDepositResponse(**response.json())





# # class UpdateProfileRequester(Requester):
# #     def put(self, payload: dict) -> UpdateProfileResponse:
# #         url = f"{self.base_url}/customer/profile"
# #         response = requests.put(
# #             url=url,
# #             json=payload,
# #             headers=self.headers,
# #         )
# #         self.response_spec(response)
# #         if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
# #             return UpdateProfileResponse(**response.json())
# #         return response  
