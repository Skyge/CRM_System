from django.forms import  forms,ModelForm
from crm import models

class CustomerModelForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"


def create_model_form(request, admin_class):
    """动态生成MODEL FORM"""
    class Meta:
        model = admin_class.model
        fields = "__all__"
    _model_form_class = type("DynamicModelForm",(ModelForm,))
    setattr(_model_form_class, "Meta", Meta)
    return _model_form_class