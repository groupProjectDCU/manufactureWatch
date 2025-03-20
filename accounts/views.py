from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm
# Create your views here.

def register(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST) #bind the form with submitted data
    if form.is_valid(): #validation
      form.save() #save new user to DB
      return redirect('login') #redirect to login page after successful registration
    else:
      form = UserRegistrationForm() #create an empty form for GET requests

#render registration template with form
return render(request, 'register.html', {'form': form}) #i cant find the web pages so i dont know the links
