from django.shortcuts import render, reverse
from django.core.mail import send_mail
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Lead, Agent
from .forms import LeadForm, CustomUserCreationForm


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
class LeadListView(ListView):
    template_name = 'leads/leads_list.html'
    queryset = Lead.objects.all()
    # the model is assigned to the context with a key of 'object_list'
    # if we want to change the key, we can do so by passing a context_object_name
    context_object_name = 'leads'


# Using class based views to create a detail page for a lead
class LeadDetailView(DetailView):
    template_name = 'leads/lead_detail.html'
    queryset = Lead.objects.all()
    context_object_name = 'lead'


# Using class based views to create a create page for a lead
class LeadCreateView(CreateView):
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
class LeadUpdateView(UpdateView):
    template_name = 'leads/lead_update.html'
    queryset = Lead.objects.all()
    form_class = LeadForm

    def get_success_url(self):
        return reverse('leads:lead_detail')


# Using class based views to create a delete page for a lead
class LeadDeleteView(DeleteView):
    template_name = 'leads/lead_delete.html'
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('leads:leads_list')
