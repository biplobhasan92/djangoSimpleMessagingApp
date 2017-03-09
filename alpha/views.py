from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from chat_app_try_1 import settings

from .models import Chat

def Login(request): #After Entering the user name and password in Login page request come here for ..
    next = request.GET.get('next', '/home/') # match them with database
    if request.method == "POST":  # But Request must be send by POST method
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)# authenticate username and password

        if user is not None: # if user is not valid
            if user.is_active: # then check it user is naw Active (Available) or not
                login(request, user)
                return HttpResponseRedirect(next)
            else: # If not Active The below message will show
                return HttpResponse("Account is not active at the moment.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)
    return render(request, "alpha/login.html", {'next': next})

def Logout(request): # when any one click Log-Out link then request will come here
    logout(request)  # After process  ...
    return HttpResponseRedirect('/login/') # The HTTP response redirect the rrequest in login page

def Home(request): #After Accessing The URL '/home' the request will come here
    c = Chat.objects.all()
    return render(request, "alpha/home.html", {'home': 'active', 'chat': c}) # And it open home.html page

def Post(request): # After write message when we click send button the request will come here
    if request.method == "POST": # check method if POST
        msg = request.POST.get('msgbox', None) # take message from request
        c = Chat(user=request.user, message=msg) #Chat object is created for save data in database
        if msg != '':
            c.save()#And Under User Message Will Save in Database
        return JsonResponse({ 'msg': msg, 'user': c.user.username })
    else:
        return HttpResponse('Request must be POST.')

def Messages(request): # by this request all message are .. show in chat panel by list
    c = Chat.objects.all()
    return render(request, 'alpha/messages.html', {'chat': c})