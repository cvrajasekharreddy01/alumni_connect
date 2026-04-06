from django.contrib import admin
from django.utils import timezone
from django.urls import path
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.urls import reverse
from .models import User, Approval

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_approved', 'is_staff')
    list_filter = ('role', 'is_approved')
    search_fields = ('email',)

@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'approve_user_button', 'approved_by', 'approved_at')
    list_filter = ('status',)
    actions = ['approve_users']

    def approve_user_button(self, obj):
        if obj.status == 'PENDING':
            return format_html(
                '<a class="button" href="{}">Approve Now</a>',
                reverse('admin:approve-user', args=[obj.pk])
            )
        return obj.status
    approve_user_button.short_description = 'Action'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('approve/<int:approval_id>/', self.admin_site.admin_view(self.approve_user_view), name='approve-user'),
        ]
        return custom_urls + urls

    def approve_user_view(self, request, approval_id):
        approval = Approval.objects.get(pk=approval_id)
        approval.status = 'APPROVED'
        approval.approved_at = timezone.now()
        approval.approved_by = request.user
        
        user = approval.user
        user.is_approved = True
        user.save()
        approval.save()
        
        self.message_user(request, f"User {user.email} has been approved.")
        return redirect('..')

    def approve_users(self, request, queryset):
        for approval in queryset:
            approval.status = 'APPROVED'
            approval.approved_at = timezone.now()
            approval.user.is_approved = True
            approval.user.save()
            approval.save()
    approve_users.short_description = "Approve selected users"
