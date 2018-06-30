from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

from website import views
from website.views import customlogin

urlpatterns = [
    url(r'^login/$', customlogin.as_view(), {'template_name': 'website/login.html'}, name='login'),
    url(r'^user/logout/$', auth_views.logout,{'next_page': '/'}, name='logout'),
    url(r'logout/^$', views.user, name='logout'),
    url(r'^topics/$', views.topics, name='topic'),
    url(r'^topics/result/(?P<query_id>[0-9]+)/$', views.results, name='result'),
    url(r'^user/result/(?P<query_id>[0-9]+)/$', views.results, name='result'),
    url(r'^$', views.home, name='home'),
    url(r'user/$',views.user,name='user'),
    url(r'signup/$',views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r"^payments/", views.payments,name='payments'),
    url(r"^checkout/(?P<query_id>[0-9]+)/$", views.checkout, name="checkout_page"),
    url(r"^add/$",views.add,name='add'),
    url(r"^fixquery/$",views.fix,name='fix'),
]