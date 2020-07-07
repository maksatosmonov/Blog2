"""itblog URL Configuration

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
from django.urls import path
from article.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", homepage, name="homepage"),
    path('authors/', authors, name="authors"),
    path("users/", users, name="users"),
    path("article/<int:id>/", article, name="article"),
    path("article/edit/<int:id>/", edit_article, name="edit-article"),
    path("article/add/", add_article, name="add-article"),
    path("author/add/", add_author, name="add-author"),
    path("profile/<int:id>/", profile, name="profile"),
    path("comment/edit/<int:id>/", edit_comment, name="edit-comment"),
    path("comment/delete/<int:id>/", delete_comment, name="delete-comment"),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
