from caki_app.models import *
from django.forms.models import model_to_dict

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