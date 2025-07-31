from django.db import models

# Create your models here.

# 장고의 models.Model을 상속받아서 데이터베이스 테이블을 클래스로 정의합니다.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)
    uploaded_image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return f"게시글 제목: {self.title} - 게시글 내용: {self.content} - 생성시간: {self.created_date} - 업데이트: {self.modified_date}"

    def get_absolute_url(self):
        return f"/blog/{self.pk}/"  # pk는 primary key로, 각 게시글을 고유하게 식별하는 값

