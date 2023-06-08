from django.shortcuts import render, redirect
from django.http import HttpResponse
from scholar.utilities.scrape import getPapers, BlockedIpException
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from twilio.rest import Client
from .models import User, PaperIndex
import os
import errno

# Create your views here.


class IndexAPIView(APIView):
    def get(self, request, format=None):
        return Response({"message": "get request handled"})


class SearchAPIView(APIView):
    def get(self, request):
        search_query = request.GET.get("q")
        papers = []
        error = None

        if search_query:
            res = getPapers(search_query, 1)
            papers = res.itemList
            error = res.error

        if error is not None:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"searchQuery": search_query, "papers": papers})


# def send_otp(request):
#     if request.method == "POST":
#         mobile_number = request.POST.get("mobile_number")
#         user, created = User.objects.get_or_create(mobile_number=mobile_number)
#         # if not created and user.is_verified:
#         # return HttpResponse("Mobile number already verified")
#         otp = generate_otp()
#         user.otp = otp
#         user.save()
#         send_otp_to_mobile_number(mobile_number, otp)
#         return redirect("scholar:verify_otp", mobile_number=mobile_number)
#     return render(request, "auth/send_otp.html")


# def verify_otp(request, mobile_number):
#     if request.method == "POST":
#         user = User.objects.get(mobile_number=mobile_number)
#         otp = request.POST.get("otp")
#         if otp == user.otp:
#             user.is_verified = True
#             user.save()
#             return redirect("scholar:search")
#         return HttpResponse("Invalid OTP")
#     return render(request, "auth/verify_otp.html", {"mobile_number": mobile_number})


# def generate_otp():
#     import random

#     return str(random.randint(100000, 999999))


# def send_otp_to_mobile_number(mobile_number, otp):
#     account_sid = settings.TWILIO_ACCOUNT_SID
#     auth_token = settings.TWILIO_AUTH_TOKEN
#     client = Client(account_sid, auth_token)
#     message = client.messages.create(
#         body=f"Your OTP is {otp}", from_=settings.TWILIO_PHONE_NUMBER, to=mobile_number
#     )
#     return message


def index(request):
    searchQuery = request.GET.get("searchQuery")
    papers = []
    error = None
    if searchQuery:
        # try:
        #     indexPapers = PaperIndex.objects.filter(journal_name__contains=searchQuery)
        #     for paper in indexPapers:
        #         print(paper.journal_name)
        # except PaperIndex.DoesNotExist:
        # return HttpResponse("does not exist")
        # papers = getResearchPapers(searchQuery, 0)
        res = getPapers(searchQuery, 5)
        papers = res.itemList
        error = res.error

    if error is not None:
        path = "templates/temp/error.html"

        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        with open("scholar/templates/temp/error.html", "w") as template:
            template.write(error)
        return render(request, "temp/error.html")

    return render(
        request,
        "scholar/index.html",
        {"searchQuery": searchQuery, "papers": papers, "error": error},
    )


def custom_404_view(request, exception=None):
    # Customize the response as per your requirements
    return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
