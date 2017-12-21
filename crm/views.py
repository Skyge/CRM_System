from django.shortcuts import render
from . import forms, models
from django.db import IntegrityError


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
            try:
                enroll_form.cleaned_data["customer"] = customer_obj
                enroll_obj = models.Enrollment.objects.create(**enroll_form.cleaned_data)
                message["register_link"] = "ddddddddd"
            except IntegrityError as e :
                enroll_obj = models.Enrollment.objects.get(customer_id=customer_obj.id,
                                                           enrolled_class_id=enroll_form.cleaned_data["enrolled_class"].id)
                enroll_form.add_error("__all__", "该用户的此条报名信息已存在，不能重复创建")
                message["register_link"] = '''请将此链接发送给客户进行填写:
                http://127.0.0.1:8000/crm/customer/enrollment/{}/'''.format(enroll_obj.id)



    else:
        enroll_form = forms.EnrollmentForm()

    return render(request, "sales/enrollment.html", {"enroll_form": enroll_form,
                                                     "customer_obj": customer_obj,
                                                     "messsage": message})
