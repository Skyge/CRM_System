from django.shortcuts import render, HttpResponse
from . import forms, models
from django.db import IntegrityError
from django.core.cache import cache

import string, random


def index(request):

    return render(request, "index.html")


def customer_list(request):

    return render(request, "sales/customers.html")


def enrollment(request, customer_id):
    customer_obj = models.Customer.objects.get(id=customer_id)
    message = {}
    if request.method == "POST":
        enroll_form = forms.EnrollmentForm(request.POST)
        if enroll_form.is_valid():
            register_link = '''请将此链接发送给客户进行填写:
                     http://localhost:8000/crm/customer/registration/{enroll_obj_id}/{random_str}/'''
            try:
                enroll_form.cleaned_data["customer"] = customer_obj
                enroll_obj = models.Enrollment.objects.create(**enroll_form.cleaned_data)
                message["register_link"] = register_link.format(enroll_obj_id=enroll_obj.id)
            except IntegrityError as e:
                enroll_obj = models.Enrollment.objects.get(customer_id=customer_obj.id,
                                                           enrolled_class_id=enroll_form.cleaned_data["enrolled_class"].id)
                enroll_form.add_error("__all__", "该用户的此条报名信息已存在，不能重复创建")
                random_str = "".join(random.sample(string.ascii_lowercase + string.digits, 8))
                cache.set(enroll_obj.id, random_str, 3000)
                message["register_link"] = register_link.format(enroll_obj_id=enroll_obj.id, random_str=random_str)
    else:
        enroll_form = forms.EnrollmentForm()

    return render(request, "sales/enrollment.html", {"enroll_form": enroll_form,
                                                     "customer_obj": customer_obj,
                                                     "message": message})


def registration(request, enroll_id, random_str):
    if cache.get(enroll_id) == random_str:
        enroll_obj = models.Enrollment.objects.get(id=enroll_id)
        if request.method == "POST":
            customer_form = forms.CustomerForm(request.POST, instance=enroll_obj.customer)
            if customer_form.is_valid():
                customer_form.save()
                enroll_obj.contract_agreed = True
                enroll_obj.save()
                return render(request, "sales/registration.html",{"status": 1})
        else:
            if enroll_obj.contract_agreed == True:
                status = 1
            else:
                status = 0
            customer_form = forms.CustomerForm(instance=enroll_obj.customer)

        return render(request, "sales/registration.html", {"customer_form": customer_form,
                                                           "enroll_obj": enroll_obj,
                                                           "status": status,})
    else:
        return HttpResponse("So foolish!想黑我,不存在的！")
