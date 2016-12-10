from django.conf.urls import url
from django.views.generic.list import ListView
from blog import views
from blog.models import About

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name = 'index'),
    url(r'^article/(?P<article_id>\d+)/$',views.ArticleDetailView.as_view(), name = 'detail'),
    url(r'^article/category/(?P<cate_id>\d+)/$', views.CategoryDetailView.as_view(), name = 'cate'),
    url(r'^full/$',views.IndexViewFull.as_view(), name = 'indexFull'),
    url(r'^about/$', ListView.as_view(template_name = 'blog_about.html', model = About), name='about'),
    url(r'^contact/$', ListView.as_view(template_name = 'blog_contact.html',model = About), name='contact'),
    url(r'^contact/send/$', views.setEmail, name = 'send'),
    url(r'^article/(?P<article_id>\d+)/comment/$', views.comment),
]
