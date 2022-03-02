import random
from django.shortcuts import reverse
from .mixins import OrganizerAndLoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from leads.models import Agent
from .forms import AgentModelForm


# Agent List View
class AgentListView(OrganizerAndLoginRequiredMixin, ListView):
    template_name = 'agents/agents_list.html'
    context_object_name = 'agents'

    def get_queryset(self):
        return Agent.objects.filter(organization=self.request.user.organization)


# Agent Create
class AgentCreateView(OrganizerAndLoginRequiredMixin, CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agents_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizer = False
        user.set_password(f"{random.randint(0, 1000000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organization=self.request.user.organization,
        )
        send_mail(
            subject='You are now an agent',
            message=f"You were created as an agent in CRM_Application by {self.request.user.username}. Please login "
                    f"to your account and change your password.",
            from_email="test@test.com",
            recipient_list=[user.email],
        )
        return super(AgentCreateView, self).form_valid(form)


# Agent Detail View
class AgentDetailView(OrganizerAndLoginRequiredMixin, DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        return Agent.objects.filter(organization=self.request.user.organization)


# Agent Update View
class AgentUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agents_list')

    def get_queryset(self):
        return Agent.objects.filter(organization=self.request.user.organization)


# Agent Delete View
class AgentDeleteView(OrganizerAndLoginRequiredMixin, DeleteView):
    template_name = 'agents/agent_delete.html'

    def get_success_url(self):
        return reverse('agents:agents_list')

    def get_queryset(self):
        return Agent.objects.filter(organization=self.request.user.organization)
