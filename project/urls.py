"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required,permission_required
from django.urls import path
from accounts.views import Registration_view,Logout_view
from pages.views import Dashboard_view,Profile_view,Management_view
from accounts.forms import Registration_Test_form,Login_form,Change_password_form,Update_form,Update_mail_form
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('logout/',Logout_view,name="logout"),
    path('admin/', admin.site.urls),
    path('register/', Registration_view.as_view(form_class=Registration_Test_form),name="register"),
    path('', Registration_view.as_view(form_class=Login_form),name="login"),
    path('home/',login_required(Dashboard_view.as_view(),login_url='/'),name="home"),
    path('profile/',login_required(Profile_view.as_view(form_class=Change_password_form,form_update_mail=Update_mail_form,form_update=Update_form),login_url='/'),name="profile"),
    path('manage/',login_required(Management_view.as_view(),login_url="/"),name="manage")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

