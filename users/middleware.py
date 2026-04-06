from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class ApprovalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Skip check for superusers or approved users
            if request.user.is_staff or request.user.is_superuser or request.user.is_approved:
                return self.get_response(request)

            # Define static exempt paths
            exempt_paths = [
                reverse('logout'),
                reverse('approval-pending'),
                '/admin/',
            ]
            
            path = request.path_info
            
            # If user is not approved and trying to access a non-exempt page
            if not any(path.startswith(url) for url in exempt_paths):
                if request.user.role != 'ADMIN':
                    return redirect('approval-pending')

        return self.get_response(request)
