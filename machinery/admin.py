from django.contrib import admin
from .models import Machinery, Collection, MachineryCollection, MachineryAssignment
from repairs.models import FaultCase, Warning

class FaultCaseInline(admin.TabularInline):
    model = FaultCase
    extra = 0
    fields = ('status', 'created_by', 'created_at', 'resolved_by', 'resolved_at')
    readonly_fields = ('created_at', 'resolved_at')
    can_delete = False
    show_change_link = True

class WarningInline(admin.TabularInline):
    model = Warning
    extra = 0
    fields = ('is_active', 'message', 'added_by', 'created_at', 'resolved_by', 'resolved_at')
    readonly_fields = ('created_at', 'resolved_at')
    can_delete = False
    show_change_link = True

@admin.register(Machinery)
class MachineryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'priority', 'description')
    list_filter = ('status',)
    search_fields = ('name',)
    inlines = [FaultCaseInline, WarningInline]
    
    # Custom actions
    actions = ['mark_as_ok', 'mark_as_warning', 'mark_as_fault']
    
    def mark_as_ok(self, request, queryset):
        queryset.update(status='OK')
    mark_as_ok.short_description = "Mark selected machines as OK"
    
    def mark_as_warning(self, request, queryset):
        queryset.update(status='WARNING')
    mark_as_warning.short_description = "Mark selected machines as WARNING"
    
    def mark_as_fault(self, request, queryset):
        queryset.update(status='FAULT')
    mark_as_fault.short_description = "Mark selected machines as FAULT"