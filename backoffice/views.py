from django.shortcuts import render
from django.views.decorators.http import require_GET,require_http_methods

@require_GET
def dashboard(request):
    return render(request,'backoffice/dashboard.html')