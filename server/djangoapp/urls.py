# djangoapp/urls.py

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # path for registration (add later if needed)

    # path for login
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),

    # path for dealer reviews view (add later)

    # path for add a review view (add later)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)