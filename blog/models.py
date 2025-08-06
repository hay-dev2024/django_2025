from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# 카테고리 모델 정의(장고가 미리 만들어주는 User와 달리 카테고리 모델은 내가 직접 만든다)
class Category(models.Model):
    name = models.CharField(max_length=100)
    # SlugField는 URL에 사용되는 짧은 이름으로, 고유해야 함(같은 카테고리가 여러 개 있으면 안됨)
    slug = models.SlugField(max_length=100,
                            unique=True,
                            allow_unicode=True # 한글도 쓰기 위해
                            )
    def __str__(self):
        return f"{self.name}----{self.slug}"

    def get_absolute_url(self):
        return f"/blog/category/{self.slug}/"


# 장고의 models.Model을 상속받아서 데이터베이스 테이블을 클래스로 정의합니다.
class Post(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)
    uploaded_image = models.ImageField(upload_to='images/', blank=True, null=True)
    uploaded_file = models.FileField(upload_to='files/', blank=True, null=True)

    def __str__(self):
        return f"게시글 제목: {self.title} - 글쓴이: {self.author} - 카테고리: {self.category} - 게시글 내용: {self.content} - 생성시간: {self.created_date} - 업데이트: {self.modified_date}"

    def get_absolute_url(self):
        return f"/blog/{self.pk}/"  # pk는 primary key로, 각 게시글을 고유하게 식별하는 값


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # 게시글이 삭제되면 댓글도 삭제됨
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True,
                                        null=True)
    updated_date = models.DateTimeField(auto_now=True,
                                          null=True)
    def __str__(self):
        return  f"댓글작성자: {self.author.username}, 댓글내용: {self.content}, 포스트이름: {self.post.title}"








