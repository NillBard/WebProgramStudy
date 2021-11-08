from articles.models import Article
from django.shortcuts import redirect, render
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def registred(request):
    if request.method == "POST":
        form = {
                'username': request.POST["username"], 
                'email': request.POST["email"],
                'password': request.POST['password']
                }
        if form["username"] and form['email'] and form['password']:
            try:
                User.objects.get(username = request.POST["username"])
                form['errors'] = u"Пользователь с таким именем уже существует"
                return render(request, 'regPage.html', {'form': form})
            except User.DoesNotExist:
                User.objects.create_user(username = request.POST["username"], 
                    email = request.POST["username"],
                    password= request.POST['password'])
                return redirect('logIn')
        else:
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'regPage.html', {'form': form})     
    else:
        return render(request, 'regPage.html', {}) 

def logIn(request):
    if request.method == "POST":
        form = {
                'username': request.POST["username"], 
                'password': request.POST['password']
                }
        if form["username"] and form["password"]:
            user = authenticate(request, username = request.POST["username"], password = request.POST["password"])
            if user is not None:
                login(request, user)
                return redirect("archive")
            else:
                form['errors'] = u"Введеный пользователь не существует"
                return render(request, 'logInPage.html', {'form': form})
        else: 
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'logInPage.html', {'form': form})
    else:
        return render(request, 'logInPage.html', {}) 

def logoutFunc(request):
    logout(request)
    return redirect('archive')

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def create_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
    # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
    # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"]:
    # если поля заполнены без ошибок
                if not Article.objects.filter(title = form['title']).exists():
                    Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    return redirect('get_article', article_id = Article.objects.count())
                else:
                    form['errors'] = u"Статья с таким названием уже существует"
                    return render(request, 'create_post.html', {'form': form})
    # перейти на страницу поста
            else:
    # если введенные данные некорректны
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
        # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})
    else:
        return redirect('regPage')