"""ProgWithAlice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from main_app.views import HomePageView, RegistrationView, LogoutView, MyPageView, MapView, change_lang, error404, \
    FirstTestView, go_to_level, Level1View, Level2View, Level3View, Level4View, Level5View
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register', RegistrationView.as_view(), name='register'),
]

urlpatterns += i18n_patterns(
    url(r'^$', HomePageView.as_view(), name='index'),
    url(r'^change_lang', change_lang, name='change-lang'),
    url(r'^logout', LogoutView.as_view(), name='logout'),
    url(r'^my_page', MyPageView.as_view(), name='my-page'),
    url(r'^map', MapView.as_view(), name='map'),
    url(r'^first_test', FirstTestView.as_view(), name='first-test'),
    url(r'^check_first_test', FirstTestView.as_view(), name='check-first-test'),

    url(r'^lvl/(?P<num>\d+)', go_to_level, name='level'),
    url(r'^lvl1', Level1View.as_view()),
    url(r'^lvl2', Level2View.as_view()),
    url(r'^lvl3', Level3View.as_view()),
    url(r'^lvl4', Level4View.as_view()),
    url(r'^lvl5', Level5View.as_view()),

    url(r'', error404)
)
