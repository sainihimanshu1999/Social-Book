from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import Profile, Post



# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username = request.user.username)
    profile_object = Profile.objects.get(user = user_object)
    context = {'profile_object':profile_object}
    return render(request,'index.html',context)

def signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already exists')
                return redirect('signup')
            else:
                user  = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #login user and redirecting to settings page

                user_login = auth.authenticate(username=username, password = password)
                auth.login(request,user_login)

                #creating a profile model for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user = user_model.id)
                new_profile.save()
                return redirect('settings') 
        else:
            messages.info(request,'Password not matching')
            return redirect('signup')


    return render(request,'signup.html')


def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('signin')


    return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            user_profile.bio = bio
            user_profile.location = location
            user_profile.profileimg = image
            user_profile.save()
        
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            user_profile.bio = bio
            user_profile.location = location
            user_profile.profileimg = image
            user_profile.save()
            
        return redirect('settings')

    context = {'user_profile':user_profile}
    return render(request, 'setting.html', context)


@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        user = request.user.username
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('index')

    return redirect('index')
