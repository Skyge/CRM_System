from django.forms import ModelForm
from . import models

class EnrollmentForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs["class"] = "form-control"

        return ModelForm.__new__(cls)

    class Meta:
        model = models.Enrollment
        fields = ["enrolled_class", "consultant"]

class CustomerForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs["class"] = "form-control"
            if field_name in cls.Meta.readonly_fields:
                field_obj.widget.attrs["disabled"] = "disabled"

        return ModelForm.__new__(cls)

    def clean_qq(self):
        if self.instance.qq != self.cleaned_data["qq"]:
            self.add_error("qq", "狐狸再狡猾,也斗不过老司机！")
        return self.cleaned_data["qq"]


    class Meta:
        model = models.Customer
        fields = "__all__"
        exclude = ["tags", "content", "memo", "status", "referral_from", "consult_course"]
        readonly_fields = ["qq", "consultant", "source"]

class PaymentForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs["class"] = "form-control"
        return ModelForm.__new__(cls)

    class Meta:
        model = models.Payment
        fields = "__all__"