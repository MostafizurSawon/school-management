from django.shortcuts import render


def home(request):
#   data = E_data.objects.all()
#   return render(request, 'home.html', {'data': data})
  return render(request, 'home.html')

def contact(request):
  return render(request, 'contact.html')