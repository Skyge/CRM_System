from  django.utils.translation import ugettext as _
from django.forms import  forms, ModelForm, ValidationError
from crm import models


class CustomerModelForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"


def create_model_form(request, admin_class):
    """动态生成MODEL FORM"""
    def __new__(cls, *args, **kwargs):
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs["class"] = "form-control"
            # field_obj.widget.attrs["maxlength"] = getattr(field_obj, "max_length") \
            #     if hasattr(field_obj, "max_length") else ""
            if field_name in admin_class.readonly_fields:
                field_obj.widget.attrs["disabled"] = "disabled"
        return ModelForm.__new__(cls)

    def default_clean(self):
        """给form默认添加clean验证"""
        error_list = []
        for field in admin_class.readonly_fields:
            field_val = getattr(self.instance, field)
            field_val_from_fronted = self.cleaned_data.get(field)
            if field_val_from_fronted != field_val:
                error_list.append(ValidationError(
                    _("Field %(field)s is readonly,data should be %(val)s"),
                    code = "invalid",
                    params = {"field": field,
                              "val": field_val
                              },))
        response = admin_class.default_form_validation(self)
        if response:
            error_list.append(response)
        if error_list:
            raise ValidationError(error_list)

    class Meta:
        model = admin_class.model
        fields = "__all__"
    attrs = {"Meta": Meta, "__new__": __new__}
    _model_form_class = type("DynamicModelForm", (ModelForm,), attrs)
    setattr(_model_form_class, "clean", default_clean)

    return _model_form_class
