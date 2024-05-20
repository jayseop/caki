from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.views import APIView
from caki_app.APIView.user_api_views import access_token_authentication
from caki_app.models import  *
from caki_app.APIView.get_others import *
from mysite.settings import MAIN_DOMAIN
import requests
import json


# 게시글 작성 api
# {
#     "contents" :{
#                     "title": "독도",
#                     "view" : "test_view",
#                     "text" : "만드는 방법",
#                     "idmember" : 13
#                 },
#     "keyword":  {
#                     "술종류" : ["보드카","진"],
#                     "당도" : ["당도1"],
#                     "도수" : ["도수1"],
#                     "음료" : []
#                 }
# }

class PostView(APIView):
    def get(self,request,idpost):
        try:
            access_token = request.headers.get('Authorization').split(' ')[1]
            user_info = access_token_authentication(access_token)
        except Exception as e:
            return{"message" : str(e)}
        idmember = user_info['idmember']

        post_instance = get_object_or_404(Post,pk = idpost)
        res = JsonResponse({
            "post_writer_info" : {
                "name" : get_post_writer(post_instance),
                "image" : get_member_image(post_instance.member_idmember),
            },
            "post_body" : model_to_dict(post_instance),
            "post_tag" : get_post_tag(post_instance),
            "post_like" : get_post_like(post_instance,idmember),
            "post_image" : get_post_image(post_instance),
            "post_date" : post_instance.date,
        })
        return res # 게시글 뷰
        



class CreatePost (APIView):
    def create_post(self,post_title,post_text,idmember):
        member_instance = get_object_or_404(Member,pk = idmember)

        new_post = Post.objects.create(
            title = post_title,
            text = post_text,
            member_idmember = member_instance
        )
        # 생성된 게시글의 기본키
        return new_post
    

    def create_tag(self,new_post,tags):
        for tag in tags:  
            tag_instance = Tag.objects.create(
                tag = tag,
                post_idpost = new_post
            )

        return tag_instance
    
    def creat_image(self,new_post,images):
        for image in images:
            image_instance = Image.objects.create(
                image_name =  image,
                image_path = image,
                post_idpost = new_post,
            )
        return image_instance

    def post(self,request):
        try:
            access_token = request.headers.get('Authorization').split(' ')[1]
            user_info = access_token_authentication(access_token)
        except Exception as e:
            return{"message" : str(e)}
        idmember = user_info['idmember']
        
        # 내용 저장
        post_body = request.data['post_body']
        # post_body = json.loads(post_body)

        new_post = self.create_post(
            post_title = post_body.get("title",''),
            post_text = post_body.get("text",''),
            idmember = idmember
            )

        # 키워드 저장
        if 'post_tag' in request.data:
            tags = request.data['post_tag']
            self.create_tag(new_post, tags)

        # 사진 저장
        if 'post_image' in request.FILES:
            images = request.FILES.getlist('post_image')
            self.creat_image(new_post,images)
            

        post_instance = new_post
        res = JsonResponse({
            "post_writer" : {
                "name" : get_post_writer(post_instance),
                "image" : get_member_image(post_instance.member_idmember),
            },
            "post_id" : post_instance.pk,
            "post_body" : model_to_dict(post_instance),
            "post_tag" : get_post_tag(post_instance),
            "post_image" : get_post_image(post_instance),
            "post_date" : post_instance.date,
            "message" : 'success'
            })

        return res
    

# 마이 페이지에서 유저 인증을 하였으니 
# 따로 유저 인증은 필요 없어보임
class DeletePost(APIView):
    def delete(self,request,idpost):
        try:
            Keep.objects.filter(post_idpost = idpost).delete()
            Like.objects.filter(post_idpost = idpost).delete()
            Tag.objects.filter(post_idpost = idpost).delete()

            # 이미지 파일 삭제
            image_instances = Image.objects.filter(post_idpost = idpost)
            for image_instance in image_instances:
                image_file_path = os.path.join(settings.MEDIA_ROOT, image_instance.image_path.name)
                if os.path.isfile(image_file_path): # 이미지 삭제
                    os.remove(image_file_path)
            curr_dir_path = os.path.dirname(image_file_path)
            if os.path.exists(curr_dir_path): # 이미지 상위 폴더 삭제
                os.rmdir(curr_dir_path)
            image_instances.delete()

            Review.objects.filter(post_idpost = idpost).delete()
            Video.objects.filter(post_idpost = idpost).delete()
            Post.objects.filter(idpost = idpost).delete()

            return JsonResponse({'message':'success'})
        except Exception as e:
            return JsonResponse({'message' : str(e)})


class EditPost(APIView):
    def edit_body(self,post_body,idpost):
        post_instance = get_object_or_404(Post,pk = idpost)
        post_instance.title = post_body['title']
        post_instance.text = post_body['text']

        post_instance.date = timezone.localtime(timezone.now())
        post_instance.save()
        # 생성된 게시글의 기본키
        return post_instance 
    

    def edit_tag(self,post_instance,new_tags):
        exist_tag_instances = Tag.objects.filter(post_idpost = post_instance.pk)
        exist_tags = []
        for exist_tag_instance in  exist_tag_instances:
            exist_tags.append(exist_tag_instance.tag)      

        for tag in exist_tags: 
            if tag not in new_tags:
                Tag.objects.get(post_idpost = post_instance.pk, tag = tag).delete()

        for tag in new_tags: 
            if tag not in exist_tags :
                Tag.objects.create(
                    tag = tag,
                    post_idpost = post_instance
                )

        return 0
    
    def edit_image(self,post_instance,new_images):
        exist_image_instances = Image.objects.filter(post_idpost = post_instance.pk)
        exist_image = []
        for exist_image_instance in  exist_image_instances:
            exist_image.append(exist_image_instance.image_name)    


        for image in exist_image: 
            if image not in new_images:
                Image.objects.get(post_idpost = post_instance.pk, image_name = image).delete()

        for image in new_images: 
            if image not in exist_image :
                Image.objects.create(
                    image_name = image,
                    image_path = image,
                    post_idpost = post_instance
                )

        return 0

    def put(self,request,idpost):
        try:
            access_token = request.headers.get('Authorization').split(' ')[1]
            user_info = access_token_authentication(access_token)
        except Exception as e:
            return{"message" : str(e)}
        
        post_instance = get_object_or_404(Post,pk = idpost)
        
        # 내용 수정
        if "post_body" in request.data:
            post_body = request.data['post_body']  
            # post_body = json.loads(post_body)     
            edit_body = self.edit_body(
                post_body = post_body,
                idpost = idpost
                )

        # 키워드 수정
        if "post_tag" in request.data:
            new_tags = request.data['post_tag']
            # new_tags = json.loads(new_tags)  
            self.edit_tag( 
                post_instance=post_instance, 
                new_tags=new_tags
            )
        
        # 사진 수정
        if "post_image" in request.FILES:
            new_images = request.FILES.getlist('post_image')
            self.edit_image( 
                post_instance = post_instance,
                new_images = new_images,
            )

        res = JsonResponse({
            "edit_post": model_to_dict(edit_body),
            "message" : 'success'
            })

        return res
    

