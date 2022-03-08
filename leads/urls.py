from django.urls import path
from .views import (
    LeadCreateView,
    LeadUpdateView,
    LeadListView,
    LeadDetailView,
    LeadDeleteView,
    AssignAgentView,
    CategoryListView,
    CategoryDetailView,
    CategoryLeadUpdateView,
    CategoryCreateView,
    LeadListJsonView,
)

app_name = 'leads'

urlpatterns = [
    path('', LeadListView.as_view(), name='leads_list'),
    path('json/', LeadListJsonView.as_view(), name='leads_list_json'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead_detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead_update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead_delete'),
    path('<int:pk>/assign_agent/', AssignAgentView.as_view(), name='assign_agent'),
    path('<int:pk>/category/', CategoryLeadUpdateView.as_view(), name='category_lead_update'),
    path('create/', LeadCreateView.as_view(), name='lead_create'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
]