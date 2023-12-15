import os
import requests

# zoom
class ZoomServices:
    def __init__(self):
        # replace with your client ID
        self.client_id = os.environ.get('CLIENT_ID')

        # replace with your account ID
        self.account_id = os.environ.get('ACCOUNT_ID')

        # replace with your client secret
        self.client_secret = os.environ.get('CLIENT_SECRET')
        
        self.auth_token_url = "https://zoom.us/oauth/token"
        self.api_base_url = "https://api.zoom.us/v2"
        
        self.access_token=self.get_access_token()
        
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
    
    def get_access_token(self):
        data={
            "grant_type": "account_credentials",
            "account_id": self.account_id,
            "client_secret": self.client_secret
        }
        response = requests.post(self.auth_token_url,auth=(self.client_id,self.client_secret),data=data)

        if response.status_code!=200:
                print("Unable to get access token")
        else:
            print("Success")
        response_data = response.json()
        access_token = response_data["access_token"]
        return access_token

    def create_meeting(self):
        print(self.client_id)
        print(self.account_id)
        print(self.client_secret)

        start_date="2023-12-28"
        start_time="17:43"
        payload = {
            "topic": "test",
            "duration": "60",
            'start_time': f'{start_date}T10:{start_time}',
            "type": 2
        }

        resp = requests.post(f"{self.api_base_url}/users/me/meetings", 
                             headers=self.headers, 
                             json=payload)

        if resp.status_code!=201:
            print("Unable to generate meeting link")
        response_data = resp.json()

        content = {
            "meeting_url": response_data["join_url"],
            "password": response_data["password"],
            "meetingTime": response_data["start_time"],
            "purpose": response_data["topic"],
            "duration": response_data["duration"],
            "message": "Success",
            "status":1
        }
        print(content)
    
    def get_participants():
        pass