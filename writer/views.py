from django.shortcuts import render, redirect, get_object_or_404
from .models import Writer
from .forms import WriterSignUpForm
from django.contrib.auth import login

def signup_writer(request):
    if request.method == "GET":
        form = WriterSignUpForm()
    else:
        form = WriterSignUpForm(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            if form.is_valid():
                new_writer = Writer.objects.create_user(full_name=request.POST['full_name'], email=request.POST['email'], username=request.POST['username'], password=request.POST['password1'], bio=request.POST['bio'])
                new_writer.save()
                login(request, new_writer)
                return redirect('PostListView')
            else:
                new_writer = None
                return render(request, 'writer/signup.html', {'form': form, 'error': 'Invalid Information'})
        else:
            return render(request, 'writer/signup.html', {'form': form, 'error': 'Passwords are not same.'})
    
    return render(request, 'writer/signup.html', {'form': form})

def writer_profile(request, name):
    profile = get_object_or_404(Writer, username=name)
    return render(request, 'writer/profile.html', {'profile': profile})