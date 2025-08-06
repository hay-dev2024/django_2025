from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.models import Post
from example.serializers import PostSerializer


# Create your views here.
def example(request):
    return render(request,
                  'example/example.html',)

@api_view(['GET', 'POST'])
def blogAPI(request):
    if request.method == 'GET': # 글 전체 리스트 보여주기
        posts = Post.objects.all() # Post 모델의 모든 객체를 가져옴
        # serializer를 사용하여 Post 객체를 JSON 형태로 변환
        postSerializer = PostSerializer(posts, many=True) # many=True -> 여러 개의 객체를 serialize할 때 사용
        return Response(postSerializer.data,
                        status=status.HTTP_200_OK) # 200_OK -> 정상 동작이라는 의미
    else: # POST 요청이 들어온 경우, 즉 새로운 글쓰기
        '''
        1. 화면에서 작성한 내용이 json 형태로 장고 서버로 넘어옴 
        2. json 형태로 넘어온 데이터를 PostSerializer를 사용하여 Post 객체로 변환(Deserialize)
        '''
        postSerializer = PostSerializer(data=request.data) # json data인 request.data를 PostSerializer에 전달
        if postSerializer.is_valid():
            postSerializer.save()  # 해당 객체를 ORM을 사용하여 DB에 저장
            return Response(postSerializer.data, # postSerializer.data와 request.data는 동일한 내용
                            status=status.HTTP_201_CREATED)
    return  Response(postSerializer.errors, # invalid한 경우
                     status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
def postAPI(request, pk):
    if request.method == 'GET':
        post = Post.objects.get(pk=pk) # pk에 해당하는 Post 객체를 가져옴
        # serialise 하는 작업이 필요하다; # PostSerializer를 사용하여 Post 객체를 JSON 형태로 변환
        postSerializer = PostSerializer(post)
        return Response(postSerializer.data, # postSerializer.data는 JSON 형태로 변환된 데이터
                        status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response("post deleted", status=status.HTTP_204_NO_CONTENT)
    else: # PUT 요청이 들어온 경우, 즉 수정
        # post = Post.objects.get(pk=pk)
        post = get_object_or_404(Post, pk=pk) # 위의 코드나 이 코드를 쓰면 된다
        postSerializer = PostSerializer(post, data=request.data)
        if postSerializer.is_valid():
            postSerializer.save()
            return Response(postSerializer.data,  # 수정된 데이터를 반환
                            status=status.HTTP_200_OK)
    return Response(postSerializer.errors, # 에러 발생 시
                    status=status.HTTP_400_BAD_REQUEST)





# 연습 api
@api_view(['GET'])
def helloAPI(request):
    return Response("hello world")

@api_view(['GET'])
def hiAPI(request):
    return Response("Hi, world!")
