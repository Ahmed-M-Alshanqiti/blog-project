from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms


# user = User.objects.all()


def Login_User(request):
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Welcome back, {username}!")
                    return redirect('/home')  
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # This string must contain ALL Tailwind classes required for the input's visual style.
        input_classes = "bg-transparent text-gray-500/80 placeholder-gray-500/80 outline-none text-sm w-full h-full"
        
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': input_classes,
            'placeholder': 'Username or Email',
        })

        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': input_classes,
            'placeholder': 'Password',
        })
        
        # Ensure labels are removed if you don't want them rendered by the template
        self.fields['username'].label = ''
        self.fields['password'].label = ''


# def Logout_user(request):


