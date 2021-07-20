from django.shortcuts import render
from django.contrib.auth.models import Permission, User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from app_users.forms import UserForm, UserProfileInfoForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView,TemplateView
from .models import user_profile, Contact
from courses.models import Standard

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        standards = Standard.objects.all()
        teachers = user_profile.objects.filter(user_type='teacher')
        context['standards'] = standards
        context['teachers'] = teachers
        return context


def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user 
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    context ={
        'registered': registered,
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'app_users/registration.html', context)  

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password= password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("<center> <h3> Account is DEACTIVATED </h3> </center>")

        else:
            messages.warning(request, 'Incorrect Username or password')
            return HttpResponseRedirect(reverse('user_login'))

    else:
        return render(request, 'app_users/login.html')
    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def hub(request):
    return render(request, 'hub.html')

def forgot_password(request):
   return render(request, 'app_users/forgot-password.html')

class ProfileView(LoginRequiredMixin, TemplateView):
   template_name = 'app_users/profile.html'
   

class ProfileUpdateView(LoginRequiredMixin, TemplateView):
   user_form = UserForm
   profile_form = UserProfileInfoForm
   template_name = 'app_users/profile-update.html'

   def post(self, request):
      post_data = request.POST or None
      file_data = request.FILES or None

      user_form = UserForm(post_data, instance=request.user)
      profile_form = UserProfileInfoForm(post_data, file_data, instance=request.user.user_profile)
      if user_form.is_valid() and profile_form.is_valid():
         user_form.save()
         profile_form.save()
         messages.success(request, 'Your Profile was successfully updated! ')
         return HttpResponseRedirect(reverse_lazy('profile'))
      context = self.get_context_data(
         user_form = user_form,
         profile_form = profile_form
      )
      return self.render_to_response(context)

   def get(self, request, *args, **kwargs):
      return self.post(request, *args, **kwargs)
         
def settings(request):
   messages.success(request, 'Welcome to your settings section')
   return render(request, 'app_users/settings.html')

class ContactView(CreateView):
    model = Contact
    fields = '__all__'
    template_name = 'app_users/contact.html'

