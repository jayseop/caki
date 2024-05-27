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


class KeywordReview(APIView):
    def post(self,request,idpost):
        access_token = request.headers.get('Authorization').split(' ')[1]
        user_info = access_token_authentication(access_token)

    
        idmember = user_info['idmember']

        member_instance = get_object_or_404(Member,pk = idmember)
        post_instance =  get_object_or_404(Post,pk = idpost)

        new_review = request.data.get('review',None)

        review_instances = Review.objects.filter(post_idpost = post_instance.pk, member_idmember = idmember )
        review_values = [review.review for review in review_instances]
        
        for review_instance in review_instances:
            review = review_instance.review
            if review not in new_review:
               review_instance.delete()
               review_values.remove(review)

        for new_keyword in new_review:
            if new_keyword not in review_values:
                Review.objects.create(
                    member_idmember = member_instance,
                    post_idpost = post_instance,
                    review = new_keyword
                )
        


        
        res = JsonResponse({
            'review' : get_post_review(post_instance,idmember),
            'message': 'success',
        })

        return res