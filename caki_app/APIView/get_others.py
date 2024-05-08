from caki_app.models import *
from django.forms.models import model_to_dict
from datetime import datetime, timedelta
import requests

# idpost를 외래키로 가진 테이블들을 하나로 통합하기 위함
# idpost를 인자로 주면 흩어져있던 테이블들을 하나로 통합후 리턴

def get_post_theme(post_instance):
    temp_instances = Temp.objects.filter(post_idpost = post_instance.pk)
    post_theme = []
    for temp in temp_instances:
        theme = temp.theme_idtheme
        post_theme.append(theme.state)
    return post_theme
    
def get_post_writer(post_instance):
    member_intance = post_instance.member_idmember
    post_writer = member_intance.nickname
    return post_writer

def get_post_like(post_instance,idmember):
    like_exists = Like.objects.filter(post_idpost = post_instance,member_idmember = idmember).exists()
    like_cnt = Like.objects.filter(post_idpost = post_instance).count()
    post_like = {
        "like_cnt" : like_cnt, # 좋아요 수
        "like_exists": True if like_exists else False # 좋아요 눌렀는지 확인
    }
    return post_like

def get_post_keep(post_instance,idmember):
    keep_exists = Keep.objects.filter(post_idpost = post_instance,member_idmember = idmember).exists()
    post_keep = {
        "keep_exists": True if keep_exists else False # 좋아요 눌렀는지 확인
    }
    return post_keep


def get_weather(nx,ny):
    try :
        servicKey = "E0xO46EqNfkCv7qI51m8bsZfMYiBEf1schQIQsWB1HemjzDnO9h+zbqGlpitexL2OS2jmOT++KTXl0cC2kjQ7A=="
        local_time = timezone.localtime(timezone.now())
        date = local_time.date()
        time = local_time.time()

        # 시간을 하나 빼고, 시간이 음수가 되지 않도록 조정
        adjusted_datetime = datetime.combine(date, time) - timedelta(hours=1)
        if adjusted_datetime.hour < 0:
            # 만약 시간이 음수가 되면 전날로 이동
            adjusted_date = date - timedelta(days=1)
            adjusted_datetime = datetime.combine(adjusted_date, adjusted_datetime.time())

        base_date = adjusted_datetime.strftime('%Y%m%d')
        base_time = adjusted_datetime.strftime('%H00')

        url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
        params ={'serviceKey' :servicKey, 
                 'pageNo' : '1', 
                 'numOfRows' : '20', 
                 'dataType' : 'json', 
                 'base_date' : base_date, 
                 'base_time' : base_time, 
                 'nx' : nx, 
                 'ny' : ny,
        }

        response = requests.get(url,params=params)
        res_dict = response.json() # json -> dict 

        item_list = res_dict['response']['body']['items']['item']
        
        curr_weather_list = []
        for item in item_list:
            if item['fcstTime'] == time.strftime("%H00"): # 현재시간만 추출
                if item['category'] == 'PTY' or item['category'] == 'SKY': # 강수량과 하늘 상황만 추출
                    curr_weather_list.append(item)

        pty_code = {0 : '강수 없음', 1 : '비', 2 : '비/눈', 3 : '눈', 5 : '빗방울', 6 : '진눈깨비', 7 : '눈날림'}
        sky_code = {1 : '맑음', 3 : '구름많음', 4 : '흐림'}

        for curr_weather in curr_weather_list: 
            if curr_weather['category'] == "PTY":
                pty_key = int(curr_weather['fcstValue']) # 강수 코드
            if curr_weather['category'] == "SKY":
                sky_key = int(curr_weather['fcstValue']) # 하늘 코드
        
        if pty_key == 0:
            weather = sky_code[sky_key]
        else :
            if pty_key == 1 or pty_key == 2 or pty_key == 5:
                weather = "비"
            if pty_key == 3 or pty_key == 6 or pty_key ==7:
                weather = "눈"


        return weather 
    
    except Exception as e:
        return str(e)