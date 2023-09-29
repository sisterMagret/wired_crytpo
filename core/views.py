from django.shortcuts import render


def index(request):
    return render(request, 'core/index.html')

def about(request):
    return render(request, 'core/about.html')

def team(request):
    return render(request, 'core/team.html')

def services(request):
    return render(request, 'core/services.html')

def why(request):
    return render(request, 'core/why.html')

def profile(request):
    return render(request, 'core/profile.html')