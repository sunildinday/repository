from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import UserRegistrationForm
from .forms import UserLoginForm
from .forms import DocumentForm
from django.http import HttpResponse
from django.db.models import Q
from user.models import Documents
#from user.forms import UserRegistrationForm

#used to submit the documet
def index(request):
    if request.user.is_authenticated():
        if request.method=='POST' and request.FILES:
            post={}
            for key in request.POST:
                post[key]=request.POST[key]
            post['user_id']=request.user.id
            post['title']=post['title'].title()
            post['abstract']=post['abstract'].title()

            form=DocumentForm(post,request.FILES)
            if form.is_valid():
                form.save()
                return render(request,'user/done.html') 
        else :
            form=DocumentForm()
            data={'sunil':'didnay'}
            return render(request,'user/home.html',{'form':form,'data':data})    
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
        user_id=request.user.id
        if author=="":
            author="#@!@#$@@!@!@!@!@@ sadbhias hdsai dhias dhasui hdius"
        if title=="":
            title="#@!@#$@@!@!@!@!@@ sdad sad sadsad sadsadsad"  
        results=Documents.objects.filter((Q(title__icontains=title)|Q(author__icontains=author))&Q(visibilty='PUBLIC')&(~Q(user_id=user_id)))
        #results=Document.objects.all()
       
        if not  results:
            msg="Empty Search Result"
            return render(request,'user/query.html',{'results':results,'msg':msg})  
        return render(request,'user/query.html',{'results':results,})    
    else:
        return render(request, 'user/login.html') 
   
def dashboard(request):
    user_id=request.user.id

    try:
        document=Documents.objects.filter(user_id=user_id)
    except:
        document=None
    return render(request,'user/dashboard.html',{'results':document,'user':user_id})
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
@csrf_protect
def ajax_dashboard(request):
    if request.is_ajax():
        q = request.GET.get('q')
        user_id=request.user.id
        if q=="":
            q="!#!B(IOSDOJI@!(*SOSasdndjsaoi j2u90usadsa d -sdusad 00828y0ds d0sysya d0say d0syd"
        try:
            document=Documents.objects.filter(Q(title__icontains=q)&Q(user_id__icontains=user_id))
           
        except:
            document=None
        ajax=True

        html= (render(request,'user/dashboard_result.html',{'results':document,'ajax':ajax}).content).decode('utf-8')
      
        
        data={'hi':html}
        return JsonResponse(data)
        #return HttpResponse({'doc':document})
        return render(request,'user/dashboard_result.html',{'results':document,'ajax':ajax})


# used to toggle the private and public visibilty of  a document
def toggle(request):
    if request.is_ajax():
        mode=request.GET.get('mode')
        document_id=request.GET.get('document_id')
        user_id=request.user.id
        document=Documents.objects.get(id=document_id,user_id=user_id)
        if mode=="PUBLIC":
            document.visibilty="PRIVATE"
        else:
            document.visibilty="PUBLIC"
        document.save()
        data={'id':document.visibilty}
        return JsonResponse(data)   

    
def about(request): 
    return render(request,'user/about.html')


def bibtex(request):

    if request.FILES:
        
        files=request.FILES[list(request.FILES.keys())[0]]
        
        bibtex_str = str(files.read())
        post={}
        index1=bibtex_str.find('title=')
        if index1!=-1:
            index2=bibtex_str.find('}',index1)
            post['title']=bibtex_str[index1+7:index2]

        index1=bibtex_str.find('author=')
        if index1!=-1:
            index2=bibtex_str.find('}',index1)
            post['author']=bibtex_str[index1+8:index2]


        index1=bibtex_str.find('abstract=')
        if index1!=-1:
            index2=bibtex_str.find('}',index1)
            post['abstract']=bibtex_str[index1+10:index2]

        index1=bibtex_str.find('publisher=')
        
        if index1!=-1:
            index2=bibtex_str.find('}',index1)
            post['publisher']=bibtex_str[index1+11:index2]

        form=DocumentForm(post)
      
        return render(request,'user/home.html',{'form':form,})   
        
     
       
# view to check for duplicates
def checker(request):
    if request.is_ajax():
        title=request.GET.get('title')
        author=request.GET.get('author')
        if author=="":
            author="#@!@#$@@!@!@!@!@@ sadbhias hdsai dhias dhasui hdius"
        if title=="":
            title="#@!@#$@@!@!@!@!@@ sdad sad sadsad sadsadsad" 
        try:
            document=Documents.objects.filter(Q(title__icontains=title)&Q(author__icontains=author))
           
        except:
            document=None
        msg={'msg':"",}
      
        if  document:
            msg={"msg":"Duplicate File with same author and title"}
            #return JsonResponse(msg)   
        return JsonResponse(msg)   

def editpost(request):
    if request.method=='POST':
        instance = get_object_or_404(Documents, id=request.POST['doc_id'])
        form = DocumentForm( instance=instance)
        return render(request,'user/editpost.html',{'form':form,'id':request.POST['doc_id']})


    else:
        logout_user(request)
       # return render(request,'user/editpost.html',{'form':form})
def savepost(request):
    if request.method=='POST':
        instance = get_object_or_404(Documents, id=request.POST['doc_id'])
        post={}
        for key in request.POST:
            post[key]=request.POST[key]
          
        post['user_id']=request.user.id
        post['title']=post['title'].title()
        post['abstract']=post['abstract'].title()
        form = DocumentForm(post, instance=instance)
        if form.is_valid():
            form.save()
            return render(request,'user/done.html') 
    else:
        logout_user(request)
