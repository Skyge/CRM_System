from django.shortcuts import render


def student_my_classes(request):

    return render(request, "student/my_classes.html")
