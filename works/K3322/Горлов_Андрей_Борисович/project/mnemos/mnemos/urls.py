"""
URL configuration for mnemos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from parse_notes import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home, name='home'),  # Главная
    path('about/', views.about, name='about'),  # О проекте
    path('contact/', views.contact, name='contact'),  # Обратная связь
    path('upload/', views.upload_file, name='upload'),  # Загрузка файла
    path('start_processing/', views.start_processing, name='start_processing'),
    path('process/', views.process_all_notes, name='process_notes'),
    path('success/', views.process_success, name='process_success'),
    path('chat/', include('chatbot.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
