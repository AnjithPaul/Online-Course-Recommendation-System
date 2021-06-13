from django.shortcuts import render,redirect
from .models import Course, Rating
from django.contrib.auth.models import User, auth
from django.contrib import messages


# Create your views here.


def courses(request):
    courselist = Course.objects.all()
    return render(request, "courses.html", {"courselist": courselist})


def coursepage(request, pk):
    course_obj = Course.objects.get(pk=pk)

    if request.user.is_anonymous:
        return render(request, "coursepage.html", {"course": course_obj})

    if Rating.objects.filter(user=request.user, course=Course.objects.get(pk=pk)).exists():
        rating_obj = Rating.objects.get(user=request.user, course=Course.objects.get(pk=pk))

        if rating_obj.rating == 1:
            rating = "Liked"
        else:
            rating = "Disliked"

    else:
        rating = "Not yet rated"

    return render(request, "coursepage.html", {"course": course_obj, "rating": rating})


def rate(request, pk):
    if request.method=="POST":
        result = request.POST["rating"]

        if result == "0":
            messages.info(request, "Invalid Rating")
            return redirect("/course/"+str(pk)+"/rate")

        else:
            if Rating.objects.filter(user=request.user, course=Course.objects.get(pk=pk)).exists():
                Rating.objects.filter(user=request.user, course=Course.objects.get(pk=pk)).delete()

            rating = Rating()
            rating.user = request.user
            rating.course = Course.objects.get(pk=pk)
            rating.rating = result
            rating.save()

        return redirect('/course/')
    else:
        return redirect('/course/'+str(pk))