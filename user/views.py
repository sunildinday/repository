from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import UserRegistrationForm
from .forms import UserLoginForm
from .forms import DocumentForm
from django.http import HttpResponse
from django.db.models import Q
from user.models import Documents,Author
#from user.forms import UserRegistrationForm

def index(request):
    if request.user.is_authenticated():
        if request.method=='POST':
          
            try:
                author=Author.objects.get(name=request.POST['author'])
            except Author.DoesNotExist:
                author=Author(request.POST['author'])
                author.save()
            post={}

            for key in request.POST:
                if key=='author':
                    post[key]=author
                    continue
                post[key]=request.POST[key]
            post['user_id']=request.user.id
        
            form=DocumentForm(post,request.FILES)
            if form.is_valid():
                form.save()
                return render(request,'user/done.html') 
        else :
            form=DocumentForm()
            return render(request,'user/home.html',{'form':form})    
    else:
        return render(request, 'user/login.html')


def logout_user(request):
    logout(request)
    form = UserLoginForm(request.POST or None)
    return render(request, 'user/login.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        #return HttpResponse(Documents._)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            
                user_id=request.user.id

                try:
                    document=Documents.objects.filter(user_id=user_id)
                except:
                    document=None
                return render(request,'user/dashboard.html',{'results':document,'user':user_id})    



            else:
                return render(request, 'user/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'user/login.html', {'error_message': 'Invalid login'})
    return render(request, 'user/login.html')

def register_user(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        form.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                
                return render(request, 'user/dashboard.html', {'name': username})
    return render(request, 'user/register.html', {'form': form})

def search(request):
    if request.user.is_authenticated():
        current_user=request.user
        return render(request,'user/search.html',{'user':current_user})    
    else:
        return render(request, 'user/login.html')    


def query(request):    
    if request.user.is_authenticated():
        author= request.GET['author']
        title= request.GET['title']
        if author=="":
            author="#@!@#$@@!@!@!@!@@"
        if title=="":
            title="#@!@#$@@!@!@!@!@@"  
        results=Document.objects.filter(Q(Title__icontains=title)|Q(Author__icontains=author))
        #results=Document.objects.all()
        return render(request,'user/query.html',{'results':results})    
    else:
        return render(request, 'user/login.html') 
   
def dashboard(request):
    user_id=request.user.id

    try:
        document=Documents.objects.filter(user_id=user_id)
    except:
        document=None
    return render(request,'user/dashboard.html',{'results':document,'user':user_id})