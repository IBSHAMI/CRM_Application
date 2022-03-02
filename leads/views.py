from django.shortcuts import render, reverse
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Lead, Agent
from .forms import LeadForm, CustomUserCreationForm
from agents.mixins import OrganizerAndLoginRequiredMixin


#  create sign up view
class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')


# Using class based views to create a landing page
class LandingPageView(TemplateView):
    template_name = 'landing_page.html'


# Using class based views to create a list of leads page
class LeadListView(LoginRequiredMixin, ListView):
    template_name = 'leads/leads_list.html'
    # the model is assigned to the context with a key of 'object_list'
    # if we want to change the key, we can do so by passing a context_object_name
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        # check if user is organizer which means they have a user profile
        # otherwise the user is an agent then we acess the user agent then user profile
        # then filter the leads based on the specific agent
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.organization)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = queryset.filter(agent__user=user)
        return queryset


# Using class based views to create a detail page for a lead
class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leads/lead_detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        # check if user is organizer which means they have a user profile
        # otherwise the user is an agent then we acess the user agent then user profile
        # then filter the leads based on the specific agent
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.organization)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = queryset.filter(agent__user=user)
        return queryset


# Using class based views to create a create page for a lead
class LeadCreateView(OrganizerAndLoginRequiredMixin, CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadForm

    def get_success_url(self):
        return reverse('leads:leads_list')

    def form_valid(self, form):
        send_mail(
            subject='New Lead Created',
            message="Check out this new lead!",
            from_email="test@test.com",
            recipient_list=["me@mail.com"]
        )
        return super(LeadCreateView, self).form_valid(form)


# Using class based views to create an update page for a lead
class LeadUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadForm

    def get_success_url(self):
        return reverse('leads:lead_detail')

    def get_queryset(self):
        user = self.request.user
        # check if user is organizer which means they have a user profile
        # otherwise the user is an agent then we acess the user agent then user profile
        # then filter the leads based on the specific agent
        queryset = Lead.objects.filter(organization=user.organization)
        return queryset


# Using class based views to create a delete page for a lead
class LeadDeleteView(OrganizerAndLoginRequiredMixin, DeleteView):
    template_name = 'leads/lead_delete.html'
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('leads:leads_list')

    def get_queryset(self):
        user = self.request.user
        # check if user is organizer which means they have a user profile
        # otherwise the user is an agent then we acess the user agent then user profile
        # then filter the leads based on the specific agent
        queryset = Lead.objects.filter(organization=user.organization)
        return queryset
