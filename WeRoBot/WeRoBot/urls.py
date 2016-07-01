"""WeRoBot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}),
    url(r'^$', 'myrobot.views.index', name='index'),
    url(r'^update', 'myrobot.views.update_database', name='update'),
    url(r'^update/print', 'myrobot.update_database_print.update_database', name='update'),
    url(r'^update/notes', 'myrobot.update_database_notes.update_database', name='update'),
    url(r'^search$', 'myrobot.views.search_database_film', name='search_film'),
    url(r'^search/developer', 'myrobot.views.search_database_developer', name='search_developer'),
    url(r'^search/dilution', 'myrobot.views.search_database_dilution', name='search_dilution'),
    url(r'^search/asa_iso', 'myrobot.views.search_database_asa_iso', name='search_asa_iso'),
    url(r'^search/result', 'myrobot.views.search_database_result', name='search_result'),
    url(r'^auth', 'myrobot.views.buyer_authenticate', name='buyer_authenticate'),
    url(r'^price-trace', 'myrobot.views.price_trace', name='price_trace'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.disable_action('delete_selected')
