from caki_app.models import *

# idpost를 외래키로 가진 테이블들을 하나로 통합하기 위함
# idpost를 인자로 주면 흩어져있던 테이블들을 하나로 통합후 리턴


def get_post_theme(post):
    temp_instances = Temp.objects.filter(post_idpost = post.pk)
    post_theme = []
    for temp in temp_instances:
        theme = temp.theme_idtheme
        post_theme.append(theme.state)
    return post_theme
    