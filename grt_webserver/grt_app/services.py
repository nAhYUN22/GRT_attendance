import os
import requests
import pytz
import datetime
from django.http import JsonResponse
from .models import MeetingTime, AccessToken, RefreshToken
from urllib.parse import urlencode

# Cisco Webex
class WebexServices:
    def __init__(self):
        self.client_id      ='C0c76a9d575a654a541fd7750ba43c03c9a6884ad1dea9827ebae97d61c6fbc00'
        self.client_secret  ='cd77d12bf55a8376ce3357f6dbe59ce09f5001f6b6d8c332a784c917c3df3122'
        self.redirect_base_uri   ='https://limhyeongseok.pythonanywhere.com/'
        self.permission_url      ='https://webexapis.com/v1/authorize?'
        self.access_token   ='MjIzYmExYTItY2Q0MS00OTkyLTgxMTEtNGUwMzZmM2Q2ZTI3NDFkYTA2M2MtZDMw_P0A1_0615a9a8-3f8a-4d33-aff0-1af12656603c'
        self.api_base_url   ="https://webexapis.com/v1"
        self.headers        ={
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
    
    def get_permission_url(self):
        params={
            "response_type":"code",
            "client_id":self.client_id,
            "redirect_uri":f"{self.redirect_base_uri}/grt/oauth/",
            "scope":'spark:kms meeting:schedules_read meeting:participants_read meeting:controls_read meeting:admin_participants_read meeting:participants_write meeting:schedules_write',
            'state': 'abcd1234',
        }
        oauth_url=self.permission_url+urlencode(params)
        print(oauth_url)
        return oauth_url
    
    def save_access_token(self,code):
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
        params={
            "grant_type":"authorization_code",
            "client_id":self.client_id,
            "client_secret":self.client_secret,
            "code":code,
            "redirect_uri":f"{self.redirect_base_uri}/grt/oauth/",
        }
        resp=requests.post(f"{self.api_base_url}/access_token",
                           headers=headers,params=params)
        data=resp.json()
        access_token = data.get("access_token")
        expires_in = data.get("expires_in")
        refresh_token = data.get("refresh_token")
        refresh_token_expires_in = data.get("refresh_token_expires_in")
        current_time = datetime.datetime.now()
        expire_time = current_time + datetime.timedelta(seconds=expires_in)
        refresh_expire_time = current_time + datetime.timedelta(seconds=refresh_token_expires_in)

        token_obj=AccessToken(
            access_token=access_token,
            expire_time=expire_time
        )
        print(access_token)
        token_obj.save()
        
        token_obj=RefreshToken(
            refresh_token=refresh_token,
            refresh_expire_time=refresh_expire_time
        )
        token_obj.save()

        return access_token
    
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
            print(type(participants))
            print("Service:")
            print(participants)
            return participants
            # return JsonResponse({"participants":participants})
        else:
            error_code=resp.status_code
            print("Failed to get participants.")
            print(resp.status_code)
            return JsonResponse({"error":"Got error"},status=error_code)
        
    def check_attendance(self, participants):
        time_now=AttendanceServices.get_time()
        
        return participants

        
class AttendanceServices:
    def __init__(self):
        self.current_time=self.get_time()
        self.current_hour=self.current_time.strftime("%H:%M")
        self.current_date=self.current_time.strftime("%m/%d")
    
    def get_time(self):
        # UTC 현재 시간
        utc_now = datetime.utcnow()

        # UTC 시간을 한국 시간대(KST, UTC+9)로 변환
        kst_timezone = pytz.timezone('Asia/Seoul')
        kst_now = utc_now.replace(tzinfo=pytz.utc).astimezone(kst_timezone)

        # print("UTC 시간:", utc_now)
        # print("한국 시간:", kst_now)
    
        return kst_now
    
    def get_registrants(self):
        register_meetings=MeetingTime.objects.filter(
            date=self.current_date,
            start_time__lte=self.current_hour,
            end_time__gte=self.current_hour
            )
        registrants=list(register_meetings.values_list('email',flat=True))
        # print(registrants)
        return registrants
    
        

# zoom
# class ZoomServices:
#     def __init__(self):
#         # replace with your client ID
#         self.client_id = os.environ.get('CLIENT_ID')

#         # replace with your account ID
#         self.account_id = os.environ.get('ACCOUNT_ID')

#         # replace with your client secret
#         self.client_secret = os.environ.get('CLIENT_SECRET')
        
#         self.auth_token_url = "https://zoom.us/oauth/token"
#         self.api_base_url = "https://api.zoom.us/v2"
        
#         self.access_token=self.get_access_token()
        
#         self.headers = {
#             "Authorization": f"Bearer {self.access_token}",
#             "Content-Type": "application/json"
#         }
        
    
#     def get_access_token(self):
#         data={
#             "grant_type": "account_credentials",
#             "account_id": self.account_id,
#             "client_secret": self.client_secret
#         }
#         response = requests.post(self.auth_token_url,auth=(self.client_id,self.client_secret),data=data)
        
#         if response.status_code!=200:
#                 print("Unable to get access token")
#         else:
#             print("Success")
#         response_data = response.json()
#         access_token = response_data["access_token"]
#         return access_token

#     def create_meeting(self):
#         print(self.client_id)
#         print(self.account_id)
#         print(self.client_secret)

#         start_date="2023-12-28"
#         start_time="17:43"
#         payload = {
#             "topic": "test",
#             "duration": "60",
#             'start_time': f'{start_date}T10:{start_time}',
#             "type": 2
#         }

#         resp = requests.post(f"{self.api_base_url}/users/me/meetings", 
#                              headers=self.headers, 
#                              json=payload)

#         if resp.status_code!=201:
#             print("Unable to generate meeting link")
#         response_data = resp.json()

#         content = {
#             "meeting_url": response_data["join_url"],
#             "password": response_data["password"],
#             "meetingTime": response_data["start_time"],
#             "purpose": response_data["topic"],
#             "duration": response_data["duration"],
#             "message": "Success",
#             "status":1
#         }
#         print(content)
        
#     def get_registrants(self,meetingId):
#         print("meetingID: "+meetingId)
#         # params={"type":"live"}
#         resp = requests.get(f"{self.api_base_url}/meetings/{meetingId}/registrants", 
#                              headers=self.headers)
#         response_data=resp.json()
#         print(response_data)
#         if resp.status_code==200:
#             participants=resp.json().get("participants",[])
#             print(participants)
#             return JsonResponse({"participants":participants})
#         else:
#             error_code=resp.status_code
#             print("Failed to get participants.")
#             print(resp.status_code)
#             return JsonResponse({"error":"Got error"},status=error_code)
    
#     def get_participants(self,meetingId):
        
#         print("meetingID: "+meetingId)
#         # params={"type":"live"}
#         resp = requests.get(f"{self.api_base_url}/metrics/meetings/{meetingId}/participants", 
#                              headers=self.headers)
#         response_data=resp.json()
#         print(response_data)
#         if resp.status_code==200:
#             participants=resp.json().get("participants",[])
#             print(participants)
#             return JsonResponse({"participants":participants})
#         else:
#             error_code=resp.status_code
#             print("Failed to get participants.")
#             print(resp.status_code)
#             return JsonResponse({"error":"Got error"},status=error_code)
