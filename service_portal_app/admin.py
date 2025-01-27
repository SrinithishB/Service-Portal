from django.contrib import admin
from .models import ServiceRequest, ServiceRequestImage,Quote

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("quote_id", "service_request", "provider", "price", "created_at")
    list_filter = ("created_at", "service_request", "provider")
    search_fields = ("service_request__description", "provider__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'customer', 'description', 'location', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__name', 'description', 'location__city')

@admin.register(ServiceRequestImage)
class ServiceRequestImageAdmin(admin.ModelAdmin):
    list_display = ('service_request', 'image', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('service_request__request_id',)
