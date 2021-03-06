from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from tickers import views

urlpatterns = [

    url(r'^tickers/$', views.TickerListCreate.as_view()),
    url(r'^tickers/(?P<pk>[0-9]+)/$', views.TickerDetail.as_view()),
    url(r'^tickersWithId/(?P<tickerId>.+)/$', views.TickerWithId.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)