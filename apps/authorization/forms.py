from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import fields

from .models import HabrUser

class HabrUserLoginForm(AuthenticationForm):
    """
    форма отвечающая за авторизацию
    """
    def __init__(self, *args, **kwargs):
        super(HabrUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = HabrUser
        fields = ("username", "password")

class HabrUserRegisterForm(UserCreationForm):
    """
    форма отвечающая за регистрацию
    """
    def __init__(self, *args, **kwargs) -> None:
        super(HabrUserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ''
    
    class Meta:
        model = HabrUser
        fields = ("email", "username", "password1", "password2")

class HabrUserEditRegisterForm(UserCreationForm):
    """
    форма отвечающая за регистрацию
    """
    def __init__(self, *args, **kwargs) -> None:
        super(HabrUserEditRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ''
    
    class Meta:
        model = HabrUser
        fields = ("email", "username", "password1", "password2")