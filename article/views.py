from django.shortcuts import render, HttpResponse, redirect
from article.models import *
from django.contrib.auth.models import User
from .forms import *
from django.db.models import Q


def homepage(request):
    if request.method == 'POST':
        key = request.POST.get("key_word")
        articles = Article.objects.filter(active=True).filter(title__contains=key) | Article.objects.filter(active=True).filter(text__contains=key) | Article.objects.filter(active=True).filter(author__name__contains=key) | Article.objects.filter(active=True).filter(comments__text__contains=key)
    else:
        if "key_word" in request.GET:
            key =request.GET.get("key_word")
            articles = Article.objects.filter(active=True).order_by("title")
        else:
            articles = Article.objects.filter(active=True)

    
    return render(request, "article/homepage.html", 
    {"articles":articles})

def article(request, id):
    article = Article.objects.get(id=id)
    article.views += 1
    user = request.user
    if not user.is_anonymous:
        article.readers.add(user)
    article.save()
    if request.method == "POST":
        if "delete_btn" in request.POST:
            article.active = False
            article.save()
            return redirect(homepage)
        elif "add_comment_btn" in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment()
                comment.user = request.user
                comment.article = article
                comment.text = form.cleaned_data["text"]
                comment.save()        

    context = {}
    context["article"] = article
    context["form"] = CommentForm()
    
    return render(
        request,
        "article/article.html",
        context
    )


def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "article/success.html")

    form = ArticleForm()
    return render(request, "article/add_article.html", {"form":form})

def edit_article(request, id):
    article = Article.objects.get(id=id)
    
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES,  instance=article)
        if form.is_valid():
            form.save()
            return render(request,"article/success.html")

    form = ArticleForm(instance=article)
    return render(request, "article/add_article.html", {"form":form})


def authors(request):
    context = {}
    context["authors_all"] = Author.objects.all()
    return render(request, "article/authors.html", context)


def add_author(request):
    if request.method == "POST":
        author = Author()
        author.name = request.POST.get("name")
        author.save()
        return render(request, "article/success.html")

    form = AuthorForm()
    return render(request, "article/add_author.html", {"form":form})


def profile(request, id):
    author = Author.objects.get(id=id)
    return render(request, "article/profile.html", {"author": author})

def users(request):
    context = {}
    context["users_all"] = User.objects.all()
    return render(request, "article/users.html", context)


def edit_comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return render(request, "article/success.html")

    form = CommentForm(instance=comment)
    return render(request, "article/comment.html", {"form":form})


def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    return render(request, "article/success.html")






# Create your views here.
