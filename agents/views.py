from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from leads.models import Agent


# Create your views here.
class AgentListView(LoginRequiredMixin, ListView):
    template_name = 'agents/agents_list.html'
    context_object_name = 'agents'

    def get_queryset(self):
        return Agent.objects.all()





