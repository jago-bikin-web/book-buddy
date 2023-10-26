from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    STATUS_CHOICES = [('M', 'Member'), ('U', 'User')]
    status = forms.ChoiceField(
        label="I am a ...",
        required=True,
        choices=STATUS_CHOICES
    )

    full_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ['status', 'full_name', 'username', 'email', 'password1']

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.status = self.cleaned_data["status"]
        user.full_name = self.cleaned_data["full_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
        
        return user