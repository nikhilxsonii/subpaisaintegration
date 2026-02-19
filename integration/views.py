from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from integration.services.pg_service import PgService

def index(request):
    return HttpResponse("Welcome to the PG index page!")

def initiate(request):
    pg_service = PgService()
    enc_data = pg_service.request().strip()
    return render(request, "pgform.html", {
        "enc_data": enc_data,
        "client_code": pg_service.client_code
    })

class PgView(viewsets.ViewSet):
    def list(self, request):
        return Response({"message": "Payment endpoint"})

@csrf_exempt
def response(request):
    pg_service = PgService()
    enc_response = request.POST.get('encResponse', '').replace(" ", "+")
    try:
        dec_data = pg_service.res(enc_response)
    except Exception as e:
        return render(request, "response.html", {"error": f"Decryption failed: {str(e)}"})
    return render(request, "response.html", {"dec_data": dec_data})
