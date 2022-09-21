from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.db.models import Q
from .models import Messages, Room,Topyc,User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import RoomForm,UserForm,MyUserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponseForbidden



def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method =='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request,'User does not exist')
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            
            messages.error(request,'Email or password did not exist')

    context = {'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')
def registerUser(request):
    page = 'register'
    form = MyUserCreationForm()
    if request.method =="POST":
        form = MyUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            print(user)
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'ann error occour during registretion')
            
            return redirect('register')
    context = {'page':page,
    'form':form}
    return render(request ,'base/login_register.html',context)
def home(request):
    q  =request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains = q) | Q(description__icontains = q))
    room_cont = rooms.count()
    topics = Topyc.objects.all()[0:5]
    room_messages = Messages.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms':rooms,
        'topics':topics,
        'room_count':room_cont,
        'room_messages':room_messages
    }
    if request.POST:
        
        return HttpResponseForbidden('base/404.html')
    return render(request,'base/home.html',context)



def custom_error_404(request, exception):
    return render(request, 'base/404.html', {})


def room(request,pk):
    room = Room.objects.get(id=pk)
    message = room.messages_set.all().order_by('created')
    participants = room.participants.all()
    if request.method=="POST":
        message = Messages.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context = {
        'room':room,
        'message':message,
        'participants':participants
    }
    return render(request,'base/room.html',context)

@login_required(login_url='loginPage')
def create_room(request):
    form = RoomForm()
    topics = Topyc.objects.all()
    if request.method =="POST":
        topic_name = request.POST.get('topic')
        topic,created = Topyc.objects.get_or_create(name=topic_name)
        room = Room.objects.create(
            host=request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
            
        )
        room.participants.add(request.user)
        room.save()
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room=form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')
        
    context = {'form':form,'topics':topics}
    return render(request, 'base/room_form.html',context)


@login_required(login_url='loginPage')
def updated_room(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    topics = Topyc.objects.all()
    if request.user != room.host:
        return HttpResponse('you are not allowed there')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topyc.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form':form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)


@login_required(login_url='loginPage')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('you are not allowed there')

    if request.method=='POST':
        room.delete()
        return redirect('home')

    context = {
        'obj':room
    }
    return render(request,'base/delete.html',context)


@login_required(login_url='loginPage')
def deleteMessage(request,pk):
    message = Messages.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('you are not allowed there')

    if request.method=='POST':
        message.delete()
        return redirect('home')

    context = {
        'obj':message
    }
    return render(request,'base/delete.html',context)



def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.messages_set.all()
    topics =Topyc.objects.all()
    context={
        'user':user,
        'rooms':rooms,
        'room_messages':room_message,
        'topics':topics
    }
    return render(request,'base/profile.html',context)


@login_required(login_url='loginPage')
def settingsUser(request):
    user=request.user
    form = UserForm(instance=user)
    if request.method =='POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile',pk=user.id)
    context={'form':form}
    return render(request,'base/edit-user.html',context)




def topicPage(request):
    q  =request.GET.get('q') if request.GET.get('q')!=None else ''
    topics = Topyc.objects.filter(name__icontains=q)
    context={
        'topics':topics
    }
    return render(request, 'base/topics.html',context)



def activityPage(request):
    room_messages = Messages.objects.filter()
    context={
        'room_messages':room_messages
    }
    return render(request, 'base/activity.html',context)