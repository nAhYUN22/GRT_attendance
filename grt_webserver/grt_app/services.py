import os
import requests
import pytz
from django.http import JsonResponse
from datetime import datetime

# Cisco Webex
class WebexServices:
    def __init__(self):
        self.access_token='NzQ3ZDFkZTctOTgyMC00ODU3LWI3YTEtZjNjMDRmMjg4NjJhMWEwZTY5YzctMjBk_P0A1_0615a9a8-3f8a-4d33-aff0-1af12656603c'
        self.api_base_url="https://webexapis.com/v1"
        self.headers={
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def create_meeting(self):
        start_time="2023-12-26T00:00"
        end_time="2023-12-26T23:00"
        
    def get_meeting_id(self, meetingnum):
        print("meetingNUM: "+meetingnum)
        params={"meetingNumber":meetingnum}
        resp=requests.get(f"{self.api_base_url}/meetings",
                          headers=self.headers,params=params)
        data=resp.json()
        print(resp)
        meetingIds=[item['id'] for item in data['items']]
        meetingId=meetingIds[0]
        
        return meetingId
        
    
    def get_participants(self,meetingId):
        print("meetingID: "+str(meetingId))
        params={"max":100,
                "meetingId":meetingId}
        resp = requests.get(f"{self.api_base_url}/meetingParticipants", 
                             headers=self.headers,params=params)
        data=resp.json()
        
        print(data)
        if resp.status_code==200:
            participants=[item['email'] for item in data['items']]
            print("Participants: ")
            print(participants)
            return JsonResponse({"participants":participants})
        else:
            error_code=resp.status_code
            print("Failed to get participants.")
            print(resp.status_code)
            return JsonResponse({"error":"Got error"},status=error_code)
        
    def check_attendance(self, participants):
        time_now=DatetimeServices.get_time()
        
        return participants

class DatetimeServices:
    def get_time():
        # UTC 현재 시간
        utc_now = datetime.utcnow()

        # UTC 시간을 한국 시간대(KST, UTC+9)로 변환
        kst_timezone = pytz.timezone('Asia/Seoul')
        kst_now = utc_now.replace(tzinfo=pytz.utc).astimezone(kst_timezone)

        print("UTC 시간:", utc_now)
        print("한국 시간:", kst_now)
    
        return kst_now

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
        
    def get_registrants(self,meetingId):
        print("meetingID: "+meetingId)
        # params={"type":"live"}
        resp = requests.get(f"{self.api_base_url}/meetings/{meetingId}/registrants", 
                             headers=self.headers)
        response_data=resp.json()
        print(response_data)
        if resp.status_code==200:
            participants=resp.json().get("participants",[])
            print(participants)
            return JsonResponse({"participants":participants})
        else:
            error_code=resp.status_code
            print("Failed to get participants.")
            print(resp.status_code)
            return JsonResponse({"error":"Got error"},status=error_code)
    
    def get_participants(self,meetingId):
        
        print("meetingID: "+meetingId)
        # params={"type":"live"}
        resp = requests.get(f"{self.api_base_url}/metrics/meetings/{meetingId}/participants", 
                             headers=self.headers)
        response_data=resp.json()
        print(response_data)
        if resp.status_code==200:
            participants=resp.json().get("participants",[])
            print(participants)
            return JsonResponse({"participants":participants})
        else:
            error_code=resp.status_code
            print("Failed to get participants.")
            print(resp.status_code)
            return JsonResponse({"error":"Got error"},status=error_code)
