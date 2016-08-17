from django.http import HttpResponse

def home(request):
    return HttpResponse("""<a href="/models/">Welcome to the Jungle!</a>""")

