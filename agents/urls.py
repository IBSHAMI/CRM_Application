from django.urls import path
from .views import (
    AgentListView,
)

app_name = 'agents'

urlpatterns = [
    path('', AgentListView.as_view(), name='agents_list'),
    # path('<int:pk>/', LeadDetailView.as_view(), name='lead_detail'),
    # path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead_update'),
    # path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead_delete'),
    # path('create/', LeadCreateView.as_view(), name='lead_create'),
]