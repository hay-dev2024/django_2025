from django.shortcuts import render

# Create your views here.

# 함수 생성
# landing 페이지를 위한 뷰 함수
def landing(request):
    return render(request,
                    'single_pages/landing.html',
                    context={
                        'title': 'Landing',
                        'name': 'Hay'
                    })


def aboutme(request):
    return render(request,
                  'single_pages/aboutme.html',
                    context={
                        'name' : 'Hay',
                    }
                  )


