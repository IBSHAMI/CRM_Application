from django.shortcuts import render, reverse
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)
from .models import Lead, Agent, Category
from .forms import LeadForm, CustomUserCreationForm, AssignAgentForm, CategoryLeadUpdateForm, CategoryForm
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
            queryset = Lead.objects.filter(organization=user.organization, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization, agent__isnull=False)
            queryset = queryset.filter(agent__user=user)
        return queryset

    # override the get_context_data method to add the user to the context
    def get_context_data(self, **kwargs):
        # get the already existing context data
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            # filter queryset based on organization and is_null
            queryset = Lead.objects.filter(organization=user.organization, agent__isnull=True)
            context.update({
                "unassigned_leads": queryset
            })
        return context


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
        lead = form.save(commit=False)
        lead.organization = self.request.user.organization
        lead.save()
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
        return reverse('leads:lead_detail', kwargs={'pk': self.get_object().pk})

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


# Agent assign view
class AssignAgentView(OrganizerAndLoginRequiredMixin, FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        return reverse('leads:leads_list')

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(pk=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


# Category List View
class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'leads/category_list.html'
    context_object_name = 'categories'

    # override the get_context_data method to add the user to the context
    def get_context_data(self, **kwargs):
        # get number of leads that are not assigned to category
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.organization)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)

        if user.is_organizer:
            context.update({
                "unassigned_lead_count": queryset.filter(category__isnull=True).count(),
            })
        return context

    def get_queryset(self):
        user = self.request.user
        # check if user is organizer which means they have a user profile
        # otherwise the user is an agent then we acess the user agent then user profile
        # then filter the leads based on the specific agent
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.organization)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)

        return queryset


# Category Detail View
class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leads/category_detail.html'
    context_object_name = 'category'

    # override the get_context_data method to add the user to the context
    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        # queryset = Lead.objects.filter(category=self.get_object())
        # or easier
        queryset = self.get_object().leads.all()
        context.update({
            "leads": queryset,
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # check if user is organizer which means they have a user profile
        # otherwise the user is an agent then we acess the user agent then user profile
        # then filter the leads based on the specific agent
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.organization)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)

        return queryset

class CategoryLeadUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'leads/category_lead_update.html'
    form_class = CategoryLeadUpdateForm

    def get_success_url(self):
        return reverse('leads:category_list')

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


# create new category
class CategoryCreateView(OrganizerAndLoginRequiredMixin, CreateView):
    template_name = 'leads/category_create.html'
    form_class = CategoryForm

    def get_success_url(self):
        return reverse('leads:category_list')

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organization = self.request.user.organization
        category.save()
        return super(CategoryCreateView, self).form_valid(form)

