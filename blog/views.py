from urllib.request import Request
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404, JsonResponse
from rest_framework.decorators import api_view
from blog.models import Post
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

from blog.serializers import PostSerializer

class UserPostView(APIView):
    
    def get(self, request, id):
        post = Post.objects.get(id=id)
        data = PostSerializer(post).data
        return Response(data)
    @csrf_exempt
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if(serializer.is_valid()): 
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    @csrf_exempt
    def patch(self, request, id, format=None):
        post = Post.objects.get(id=id)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    @csrf_exempt
    def delete(self, request, id, format=None):
        post = Post.objects.get(id=id)
        post.delete()
        return Response(status=204)
    
class UserPostsView(APIView):
    @csrf_exempt
    def get(self, request, username):
        post = Post.objects.filter(author__username=username)
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)