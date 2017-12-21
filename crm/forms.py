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