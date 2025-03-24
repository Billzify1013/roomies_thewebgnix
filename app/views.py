from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

def hotel_view(request):
    return render(request,'hotel_view.html')