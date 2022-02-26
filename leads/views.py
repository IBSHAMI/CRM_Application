from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Lead, Agent
from .forms import LeadForm


# Using class based views
class LandingPageView(TemplateView):
    template_name = 'landing_page.html'


def landing_page(request):
    return render(request, 'landing_page.html')


def show_leads_list(request):
    # get all leads information as queryset
    leads = Lead.objects.all()
    context = {
        'leads': leads
    }
    return render(request, 'leads/leads_list.html', context)


# view lead details
def lead_detail(request, pk):
    # get lead information by primary key
    lead = Lead.objects.get(pk=pk)
    context = {
        'lead': lead
    }
    return render(request, 'leads/lead_detail.html', context)


# create a new lead
def lead_create(request):
    form = LeadForm(request.POST or None)

    # if form is valid and request is submitted then save new lead to database
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/leads')

    context = {
        'form': LeadForm()
    }
    return render(request, 'leads/lead_create.html', context)


# update lead information
def lead_update(request, pk):
    # get lead information by primary key
    lead = Lead.objects.get(pk=pk)
    form = LeadForm(request.POST or None, instance=lead)

    # if form is valid and request is submitted then update lead information
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/leads')

    context = {
        'form': form,
        'lead': lead,
    }
    return render(request, 'leads/lead_update.html', context)


# delete lead
def lead_delete(request, pk):
    # get lead information by primary key
    lead = Lead.objects.get(pk=pk)
    lead.delete()
    return redirect('/leads')
