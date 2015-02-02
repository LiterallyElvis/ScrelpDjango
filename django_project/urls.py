from django.conf.urls import patterns, include, url
from screlp import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    # Examples:
    # url(r'^$', 'django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r"^admin/", include(admin.site.urls)),
    url(r"^$", views.home, name="index"),
    url(r"^search/", views.result),
    url(r"^autocomplete/", views.autocomplete),
    url(r"^login/", views.login),
    url(r"^logout/", views.logout),
    url(r"^register/", views.register),
    url(r"^reset/", views.reset_demo_access),
    url(r"^beta/", views.beta)
)
