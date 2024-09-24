from django.shortcuts import render
from django.http import HttpResponse

# View to render the hello.html template
def welcome_view(request):
    return render(request, 'welcome.html')