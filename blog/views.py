from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # 로그인한 사용자만 접근할 수 있도록 함
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .forms import PostForm, CommentForm
from .models import Post, Category, Comment

# Class-based views
class PostListView(ListView):
    model = Post
    # ordering = ['-created_date'] # 최신 게시글이 위에 오도록 정렬
    ordering = ['-pk'] # 위와 동일한 기능

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category', 'uploaded_image', 'uploaded_file']

    # 비어있는 author 처리(로그인한 사용자의 author가 자동으로 설정되기 때문에 forms.py에서 삭제했음)
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreateView, self).form_valid(form)
        else:
            return redirect('/blog/')

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'category', 'uploaded_image', 'uploaded_file']
    # template_name = 'blog/postupdateform.html'  # 템플릿 파일 경로 지정

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/'  # 삭제 후 리다이렉트할 URL



# Create your views here.
# function-based views
# 함수 생성
def index(request):
    posts = Post.objects.all().order_by('-pk')  # 작성한 포스트를 모두 가져옴; select * from blog_post; 과 동일함. 게시물을 역순으로 정렬 : .order_by('-pk')
    categorys = Category.objects.all()
    return render(request,
                  'blog/index.html',
                  context={'posts': posts,
                           'categorys': categorys,
                           })


def category(request, slug):
    categorys = Category.objects.all()
    if slug == "no_category":
        posts = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        posts = Post.objects.filter(category=category)
    return render(request,
                  'blog/index.html',
                  context={'posts': posts,
                           'categorys': categorys,
                            })


# 로그인한 사용자만 블로그 상세페이지를 볼 수 있도록 데코레이터 설정; 로그인 안한 경우에는 로그인 페이지로 리다이렉트
@login_required(login_url='/accounts/google/login/')
def detail(request, pk):
    post = Post.objects.get(pk=pk)  # pk(primary key)에 해당하는 포스트를 가져옴
    categorys = Category.objects.all()
    comments = Comment.objects.filter(post=post)  # 해당 포스트에 달린 댓글들을 가져옴; select * from blog_comment where post_id=pk;
    # comments = Comment.objects.get(post=post)
    return render(request,
                  'blog/detail.html',
                  context={'post': post,
                           'categorys': categorys,
                           'comments': comments,
                           })


# 블로그 글쓰기 로직
# GET과 POST 요청을 모두 처리하는 함수
@login_required(login_url='/accounts/google/login/')
def create(request):
    categorys = Category.objects.all()
    if request.method == 'POST':
        # 글 작성하다가 제출 버튼을 누른 경우
        postform = PostForm(request.POST, request.FILES)
        if postform.is_valid():
            # 폼이 유효한 경우, 즉 입력값이 올바른 경우
            post1 = postform.save(commit=False) # commit=False는 아직 DB에 저장하지 않고 메모리 상에만 존재하는 상태; 객체를 생성만 함
            post1.author = request.user
            post1.save() # DB에 저장
            # postform.save()
            return redirect('/blog/') # 글 목록 페이지로 리다이렉트
    else: # GET 요청이 들어온 경우(새글쓰기 버튼을 눌러서 create()함수로 들어온 경우; 맨 처음에 빈 폼을 보여주는 경우; 글 작성 페이지를 처음 열었을 때)
        postform = PostForm() # 새 인스턴스를 생성
    return render(request,
                  template_name='blog/postform.html',
                  context={'postform': postform,
                           'categorys': categorys,
                           })


# 자동으로 글이 작성되게 해보기
def createfake(request):
    post = Post() # Post 객체를 생성
    post.title = "새싹 용산"
    post.content = "오늘은 목요일이다."
    post.save()
    return redirect('/blog/')

@login_required(login_url='/accounts/google/login/')
def delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete() # 해당 포스트를 삭제
    return redirect('/blog/') # 글 목록 페이지로 리다이렉트
    # return redirect('index') # 이렇게 써도 됨; index는 urls.py에서 정의한 이름이다. urls.py에서 name='index'로 지정해주면 된다.)

# pk -> post의 pk
@login_required(login_url='/accounts/google/login/')
def update(request, pk):
    post = Post.objects.get(pk=pk) # 수정하고 싶은 포스트를 가져옴
    if request.method == 'POST':
        postform = PostForm(request.POST, request.FILES, instance=post)
        if postform.is_valid(): # 폼이 유효한 경우
            postform.save()
            return redirect('/blog/')
    else:
        postform = PostForm(instance=post)

    return render(request,
                  template_name='blog/postupdateform.html',
                  context={'postform': postform,})


# Comment CRUD 기능 추가
@login_required(login_url='/accounts/google/login/')
def comment_create(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content and request.user.is_authenticated:
            Comment.objects.create(post=post, content=content, author=request.user)
    return redirect(f'/blog/{pk}/')


@login_required(login_url='/accounts/google/login/')
def comment_update(request, pk):
    comment = Comment.objects.get(pk=pk) # 코멘트를 수정하거나 삭제할때는 코멘트의 pk를 사용한다.
    post = comment.post # 해당 댓글이 달린 포스트를 가져옴
    if request.method == 'POST':
        commentform = CommentForm(request.POST, instance=comment)
        if commentform.is_valid():
            commentform.save(commit=False)
            commentform.author = request.user
            commentform.save()
            return redirect(f'/blog/{post.pk}/')
    else:
        commentform = CommentForm(instance=comment)

    return render(request,
                  template_name='blog/comment_updateform.html',
                  context={'commentform': commentform,})

@login_required(login_url='/accounts/google/login/')
def comment_delete(request, pk):
    comment = Comment.objects.get(pk=pk)
    post = comment.post
    comment.delete()
    return redirect(f'/blog/{post.pk}/')


