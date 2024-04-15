from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import LoginView
from .forms import LoginForm, CreateUserForm
from django.contrib.auth import get_user_model, login, logout

User = get_user_model()


class RegistrationFormView(FormView):
    template_name = 'users/register.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('home')
    model = User

    def get(self, request, *args, **kwargs):
        """ 
        check if user already login redierct to home page
        """
        return redirect('home') if request.user.is_authenticated else super().get(request, *args, **kwargs)
        

    def generate_username(self, form):
        """Generate Unique Username"""
        
        data = form.cleaned_data
        username = f"{ data['first_name'] }{ data['last_name'] }"
        exists_users = User.objects.filter(username=username)
        
        if exists_users.exists():
            users_counter = len(exists_users)
            while 1:
                username = f"{ data['first_name'] }{ data['last_name'] }{ users_counter }"
                exists_users = User.objects.filter(username=username)
                if exists_users.exists():
                    users_counter+=1
                else: break
        
        return username
                
    
    def form_valid(self, form):
        """ Add Unique Userame To Form
            Make User Login After Reisterion Process : If you will add email confirmation delete this process
        """
        user = form.save(commit=False)
        user.username = self.generate_username(form)
        user.save()
        
        if user is not None:
            login(self.request, user)
        
        return super().form_valid(form)


class LoginFormView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        """ 
        check if user already login redierct to home page
        if user redirect from some place in site render login page with message
        """        
        if request.user.is_authenticated and '?next=/' not in request.get_full_path():
            return redirect('home')
        return super().get(request, *args, **kwargs) 


def logout_view(request):
    logout(request)
    return redirect('home') 

    
    