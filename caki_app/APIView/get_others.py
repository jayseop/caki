from caki_app.models import *
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Count
from pprint import pprint
import requests
from mysite.settings import MAIN_DOMAIN, STATIC_URL,STATIC_ROOT

# idpost를 외래키로 가진 테이블들을 하나로 통합하기 위함
# idpost를 인자로 주면 흩어져있던 테이블들을 하나로 통합후 리턴

def get_post_tag(post_instance):
    tag_instances = Tag.objects.filter(post_idpost = post_instance.pk)
    post_tag = []
    for tag_instance in tag_instances:
        post_tag.append(tag_instance.tag)
    return post_tag
    
def get_post_writer(post_instance):
    member_intance = post_instance.member_idmember
    post_writer = member_intance.nickname
    return post_writer

def get_post_like(post_instance,idmember):
    like_exists = Like.objects.filter(post_idpost = post_instance,member_idmember = idmember).exists()
    like_cnt = Like.objects.filter(post_idpost = post_instance).count()
    post_like = {
        "cnt" : like_cnt, # 좋아요 수
        "exists": True if like_exists else False # 좋아요 눌렀는지 확인
    }
    return post_like

def get_post_keep(post_instance,idmember):
    keep_exists = Keep.objects.filter(post_idpost = post_instance,member_idmember = idmember).exists()
    post_keep = {
        "exists": True if keep_exists else False # 저장 눌렀는지 확인
    }
    return post_keep


def get_weather(nx,ny):
    try :
        servicKey = "E0xO46EqNfkCv7qI51m8bsZfMYiBEf1schQIQsWB1HemjzDnO9h+zbqGlpitexL2OS2jmOT++KTXl0cC2kjQ7A=="
        local_time = timezone.make_aware(timezone.now())
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
        params ={
            'serviceKey' :servicKey, 
            'pageNo' : '1', 
            'numOfRows' : '25', 
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

        # pty_code = {0 : '강수 없음', 1 : '비', 2 : '비/눈', 3 : '눈', 5 : '빗방울', 6 : '진눈깨비', 7 : '눈날림'}
        # sky_code = {1 : "맑음", 3 : "구름많음", 4 : "흐림"}

        for curr_weather in curr_weather_list: 
            if curr_weather['category'] == "PTY":
                pty_key = int(curr_weather['fcstValue']) # 강수 코드
            if curr_weather['category'] == "SKY":
                sky_key = int(curr_weather['fcstValue']) # 하늘 코드
        
        if pty_key == 0:
            if sky_key == 1:
                weather = "맑음"
            elif sky_key == 3:
                weather = "구름많음"
            elif sky_key == 4:
                weather = "흐림"
        else :
            if pty_key in [1,2,5]:
                weather = "비"
            if pty_key in [3,6,7]:
                weather = "눈"


        return weather 
    
    except Exception as e:
        return "정보 없음"
    
def get_member_image(idmember):
    try:
        member_image_path = get_object_or_404(Member,pk = idmember).image_path
        return MAIN_DOMAIN + member_image_path.url
    except:
        return MAIN_DOMAIN + os.path.join(STATIC_URL, "user.png")


def get_post_image(post_intance):
    image_intances = Image.objects.filter(post_idpost = post_intance.pk)
    image_url = []
    for image_intance in image_intances:
        image_url.append(MAIN_DOMAIN + image_intance.image_path.url)
    if image_url:
        return image_url
    else:    
        return MAIN_DOMAIN + os.path.join(STATIC_URL, "cocktail.png")


def get_post_review(post_instance,idmember):
    post_reivew = Review.objects.filter(post_idpost = post_instance.pk)
    keyword_cnt_q = post_reivew.values('review').annotate(count=Count('review'))
    review = []
    for keyword_cnt in keyword_cnt_q:
        keyword = keyword_cnt.get('review')
        cnt = keyword_cnt.get('count')
        info = {
            "keyword" : keyword,
            "cnt" : cnt,
            "exists" : post_reivew.filter(member_idmember = idmember, review = keyword).exists()
        }
        review.append(info)
    return review
    

def get_post_preview(post_instance):
    preview = {
        "writer_nickname" : post_instance.member_idmember.nickname,
        "post_id" : post_instance.idpost,
        "post_title" : post_instance.title,
        "post_image" :  get_post_image(post_instance),
        "post_tag" : get_post_tag(post_instance),
        "post_like" : Like.objects.filter(post_idpost = post_instance.pk).count(),
    }
    return preview
