from django.conf.urls import url
from Users import views


urlpatterns = [
    url(r'^profiles/$', views.ProfilesListView.as_view()),
    url(r'^profiles/(?P<user_id>\d+)/$', views.ProfileDetailView.as_view()),
    url(r'^profiles/(?P<user_id>\d+)/add_awards/$', views.AddNewAwardView.as_view()),
]
