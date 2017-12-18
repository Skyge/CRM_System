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
            if not hasattr(admin_class, "is_add_form"):
                if field_name in admin_class.readonly_fields:
                    field_obj.widget.attrs["disabled"] = "disabled"

            if hasattr(admin_class, "clean_{}".format(field_name)):
                field_clean_func = getattr(admin_class, "clean_{}".format(field_name))
                setattr(cls, "clean_{}".format(field_name), field_clean_func)

        return ModelForm.__new__(cls)

    def default_clean(self):
        """给form默认添加clean验证"""
        error_list = []
        if self.instance.id:
            for field in admin_class.readonly_fields:
                field_val = getattr(self.instance, field)

                if hasattr(field_val, "select_related"):
                    m2m_objs = getattr(field_val, "select_related")().select_related()
                    m2m_val = [i[0] for i in m2m_objs.values_list("id")]
                    set_m2m_val = set(m2m_val)
                    set_m2m_val_from_fronted = set([i.id for i in self.cleaned_data.get(field)])
                    if set_m2m_val_from_fronted != set_m2m_val:
                        error_list.append(ValidationError(
                            _("Field %(field)s is readonly"),
                            code="invalid",
                            params={"field": field},))
                    continue
                field_val_from_fronted = self.cleaned_data.get(field)
                if field_val_from_fronted != field_val:
                    error_list.append(ValidationError(
                        _("Field %(field)s is readonly,data should be %(val)s"),
                        code = "invalid",
                        params = {"field": field,
                                  "val": field_val
                                  },))
        if admin_class.readonly_table:
            raise ValidationError(
                        _("Table is read only,cannot be modify or added!"),
                        code = "invalid",)
        response = admin_class.default_form_validation(self)
        if response:
            error_list.append(response)
        if error_list:
            raise ValidationError(error_list)

    class Meta:
        model = admin_class.model
        fields = "__all__"
    attrs = {"Meta": Meta}
    _model_form_class = type("DynamicModelForm", (ModelForm,), attrs)
    setattr(_model_form_class, '__new__', __new__)
    setattr(_model_form_class, "clean", default_clean)

    return _model_form_class
