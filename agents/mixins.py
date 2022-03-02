from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


# to prevent agents from accessing the some pages even if they hardcode the url
class OrganizerAndLoginRequiredMixin(AccessMixin):
    """
    CBV Mixin which verifies that the current user is authenticated and is organizer.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organizer:
            return redirect('leads:leads_list')
        return super().dispatch(request, *args, **kwargs)
