from django.shortcuts import render
from django.views.decorators.http import require_GET

@require_GET
def lobby(request):
    return render(request, "hotel/lobby.html")
