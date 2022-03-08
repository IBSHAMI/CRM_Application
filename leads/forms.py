from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Lead, User, Agent, Category


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        fields_classes = {"username": UsernameField}


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
            'description',
            'phone',
            'email',
            'profile_pic',
        )


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        agents = Agent.objects.filter(organization=request.user.organization)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


class CategoryLeadUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category',
        )


# create new category by organizer
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
        )
