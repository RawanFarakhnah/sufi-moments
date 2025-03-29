from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Registration successful! Please log in.'))
        return response

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _('You have successfully logged in!'))
                return redirect('home')  # Change 'home' to your desired redirect URL
        else:
            messages.error(request, _('Invalid email or password.'))
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, _('You have been logged out.'))
    return redirect('accounts:login')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')