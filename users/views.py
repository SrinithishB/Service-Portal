from django.shortcuts import render,redirect
from .forms import NewRegisterForm
from django.contrib.auth.models import User
from .models import Profile,Location
from django.http import HttpResponse

from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        try:
            profile =request.user.profile
        except Profile.DoesNotExist:
            return redirect('profile/edit')
        if profile.user_type == 'Customer':
            return redirect('Service Portal:customer')
        elif profile.user_type == 'Service Provider':
            return redirect('Service Portal:provider') 
    return redirect('user:register')

def register(request):
    if request.method=="POST":
        form=NewRegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            return redirect('user:login')
    else:
        form=NewRegisterForm()
    context={
        'form':form
    }
    return render(request,'users/register.html',context)


def profile(request):
    return render(request,'users/profile.html')

@login_required
def edit_profile(request):
    try:
        locations = Location.objects.all()
        profile =request.user.profile
    except Profile.DoesNotExist:
        profile=None
    if request.method=='POST':
        if profile:
            profile.name=request.POST.get('name')
            profile.phone_no=request.POST.get('phone')
            profile.user_type=request.POST.get('user_type')
            location_id = request.POST.get('location')  # Get the selected location
            if location_id:
                profile.location = Location.objects.get(location_id=location_id)  # Set the location based on selected ID

            if request.FILES.get('image'):
                profile.profile_image = request.FILES['image']
            profile.save()      
        else:
            user=request.user
            name=request.POST.get('name')
            phone=request.POST.get('phone')
            
            user_type=request.POST.get('user_type')
            location_id = request.POST.get('location')
            location = Location.objects.get(location_id=location_id) if location_id else None
            try:
                image=request.FILES['image']
                profile = Profile(user=user, name=name, phone_no=phone, user_type=user_type, location=location, profile_image=image)
            except:
                profile = Profile(user=user, name=name, phone_no=phone, user_type=user_type, location=location)
            profile.save()
        return redirect('user:profile')
    user_types = ['Customer', 'Service Provider']
    context={
        'profile':profile,
        'user_types': user_types,
        'locations': locations
    }

    return render(request,'users/edit_profile.html',context)
    # return HttpResponse("Hello, World!")

def check_profile(request):
    try:
        profile =request.user.profile
    except Profile.DoesNotExist:
        return redirect('profile/edit')

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        # Call the parent form_valid to log the user in
        response = super().form_valid(form)
        try:
            profile =self.request.user.profile
        except Profile.DoesNotExist:

            return redirect(reverse('user:edit_profile'))
        return redirect(reverse('user:index')) 