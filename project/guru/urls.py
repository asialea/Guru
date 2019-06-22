
from . import views
from django.conf.urls import url,re_path
from rest_framework import routers
from django.urls import include

app_name = 'guru'
urlpatterns = [
    #viewsets
    url('^api/users/$', views.UserViewSet.as_view() ),
    # Authentication
    url('^auth/register/$', views.RegistrationView.as_view()),
    url('^auth/login/$', views.LoginView.as_view()),
    url('^auth/user/$', views.UserView.as_view()),
    url('^auth/logout/$', views.LogoutView.as_view()),
    url('^auth/update/$', views.UpdateUserView.as_view()),

    # Edit user profile
    url('^api/education/$',views.EducationView.as_view()),
    url('^api/education/(?P<id>\d+)', views.EducationView.as_view()),
    url('^api/aboutUser/$', views.AboutUserView.as_view()),
    url('^api/avi/(?P<id>\d+)', views.AviView.as_view()),
    url('^api/interests/$',views.UserInterestsView.as_view()),
    url('^api/interests/(?P<id>\d+)', views.UserInterestsView.as_view()),
    # View user profile
    url('^api/user/(?P<username>[a-zA-Z0-9_.-s]+)/$',views.ReadUserView.as_view()),
    url('^api/aboutUser/(?P<username>[a-zA-Z0-9_.-s]+)/$',views.ReadAboutUserView.as_view()),
    url('^api/edu/(?P<username>[a-zA-Z0-9_.-s]+)/$',views.EducationView.as_view()),
    url('^api/work/(?P<username>[a-zA-Z0-9_.-s]+)/$',views.WorkView.as_view()),
    url('^api/skills/(?P<username>[a-zA-Z0-9_.-s]+)/$',views.UserSkillsView.as_view()),
    url('^api/interests/(?P<username>[a-zA-Z0-9_.-s]+)/$',views.UserInterestsView.as_view()),
    url('^api/rec/(?P<username>[a-zA-Z0-9_.-s]+)/$', views.RecommendationView.as_view()),

    # Search
    url('^api/filter/$',views.FilterUserView.as_view()),
    # Forum
    url('^api/category/$',views.CategoryView.as_view()),
    url('^api/topic/(?P<cat_id>\d+)',views.TopicView.as_view()),
    url('^api/post/(?P<top_id>\d+)',views.PostView.as_view()),
    url('^api/user_topics/$', views.UserTopicView.as_view()),
    url('^api/recent_topics/$', views.RecentTopicView.as_view()),
    url('^api/likes/(?P<post_id>\d+)', views.LikesView.as_view()),

    url('^api/email/$', views.EmailView.as_view()),

]
