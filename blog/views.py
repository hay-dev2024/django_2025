from django.shortcuts import render
from .models import Post

# Create your views here.

# 함수 생성
def index(request):
    posts = Post.objects.all()  # 작성한 포스트를 모두 가져옴; select * from blog_post; 과 동일함.
    return render(request,
                  'blog/index.html',
                  context={'posts': posts} # posts를 화면에 보여주기
                  )

def detail(request, pk):
    post = Post.objects.get(pk=pk)  # pk(primary key)에 해당하는 포스트를 가져옴
    return render(request,
                  'blog/detail.html',
                  context={'post': post}
                  )

