from django.conf.urls import url
from Users import views


urlpatterns = [
    url(r'^profiles/$', views.ProfilesListView.as_view()),
    url(r'^profiles/register/$', views.SignUpView.as_view()),
    url(r'^profiles/(?P<user_id>\d+)/$', views.ProfileDetailView.as_view()),
    url(r'^profiles/(?P<user_id>\d+)/add_achievement/$', views.AddNewAchievementView.as_view()),
    url(r'^profiles/(?P<user_id>\d+)/buy_pin/$', views.BuyPinView.as_view()),
    url(r'^profiles/(?P<user_id>\d+)/update_rating/$', views.ChangeRatingView.as_view()),
]
