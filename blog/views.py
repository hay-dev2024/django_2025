from django.shortcuts import render, redirect

from .forms import PostForm
from .models import Post

# Create your views here.

# 함수 생성
def index(request):
    posts = Post.objects.all().order_by('-pk')  # 작성한 포스트를 모두 가져옴; select * from blog_post; 과 동일함. 게시물을 역순으로 정렬 : .order_by('-pk')
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

def create(request):
    if request.method == 'POST':
        # 글 작성하다가 제출버튼을 누른 경우
        postform = PostForm(request.POST, request.FILES)
        if postform.is_valid():
            # 폼이 유효한 경우, 즉 입력값이 올바른 경우
            post1 = postform.save(commit=False) # commit=False는 아직 저장하지 않고, 객체를 생성만 함
            post1.title = post1.title + " 바나나파인애플이다!"
            post1.save()
            # postform.save()
            return redirect('/blog/') # 글 목록 페이지로 리다이렉트
    else:
        # get 요청이 들어온 경우(맨 처음에 빈 폼을 보여주는 경우; 글 작성 페이지를 처음 열었을 때)
        postform = PostForm()
    return render(request,
                  template_name='blog/postform.html',
                  context={'postform': postform}
                  )


# 자동으로 글이 작성되게 해보기
def createfake(request):
    post = Post() # Post 객체를 생성
    post.title = "새싹 용산"
    post.content = "오늘은 목요일이다."
    post.save()
    return redirect('/blog/')


