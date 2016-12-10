from  django.conf.urls import url,include
from django.contrib import admin
from . import views
from django.utils import timezone
now = timezone.now()

urlpatterns = [
    url(r'^/accounts',include('django.contrib.auth.urls')),
    url(r'^$', views.FingerIndex.as_view(), name='finger_index'),
    url(r'^admin/',admin.site.urls),
    url(r'^get/$',views.getFinger),
    url(r'^get/SCK/$',views.getFingerBack),
    url(r'^put/$', views.putFinger),
    url(r'^do_atendance/$',views.FingerAtendance),
    url(r'^atendance/$', views.ShowAllAtendance.as_view(),{'year':str(timezone.now().year),'month':str(timezone.now().month)}),
    url(r'^atendance/(?P<year>\d+)/(?P<month>\d+)/$',views.ShowAllAtendance.as_view() ),
    url(r'^atendance/(?P<student_id>\d+)/$',views.ShowOneStudentAtendance.as_view(),
                                            {'year':str(timezone.now().year),'month':str(timezone.now().month)},
                                             name='show_atendance'),
    url(r'^atendance/(?P<year>\d+)/(?P<month>\d+)/(?P<student_id>\d+)',views.ShowOneStudentAtendance.as_view()),
    url(r'^atendance/(?P<year>\d+)/(?P<month>\d+)/search/$',views.student_Search),
    url(r'^atendance/sort/',views.atendance_sort.as_view()),
]
