from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm


User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "autocomplete": "off",
                "placeholder": "enter your password"
            }
        )
    )


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'birthday',
        ]
        form_control = {"class": "form-control"}
        widgets = {
            "username": forms.TextInput(attrs=form_control),
            "first_name": forms.TextInput(attrs=form_control),
            "last_name": forms.TextInput(attrs=form_control),
            "email": forms.EmailInput(attrs=form_control),
            "phone": forms.TextInput(attrs=form_control),
            "birthday": forms.DateInput(attrs={"class": "form-control", "type": "date"})
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "avatar",
            "email",
            "first_name",
            "last_name",
            "birthday",
            "phone",
            "is_private"
        )
        widgets = {
            "avatar": forms.FileInput(
                attrs={"class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "birthday": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format=("%Y-%m-%d")
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "is_private": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'avatar' in self.changed_data and not instance.avatar:
            instance.avatar = self.changed_data['avatar']
        if commit:
            instance.save()
        return instance
    

class UserPasswordChangeForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]
