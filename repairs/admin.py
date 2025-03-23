from django.contrib import admin
from .models import FaultCase, FaultNote, Warning

class FaultNoteInline(admin.TabularInline):
    model = FaultNote
    extra = 0
    fields = ('note', 'user', 'created_at')
    readonly_fields = ('created_at',)
    can_delete = False
    show_change_link = True


@admin.register(FaultCase)
class FaultCaseAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'machine', 'created_at', 'status', 'created_by')
    list_filter = ('status', 'created_at')
    search_fields = ('machine__name', 'created_by__username')
    date_hierarchy = 'created_at'
    inlines = [FaultNoteInline]

@admin.register(FaultNote)
class FaultNoteAdmin(admin.ModelAdmin):
    list_display = ('case', 'user', 'note', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('case__machine__name', 'note')
    date_hierarchy = 'created_at'

@admin.register(Warning)
class WarningAdmin(admin.ModelAdmin):
    list_display = ('warning_id', 'machine', 'message', 'added_by', 'created_at')
    search_fields = ('machine__name', 'message')
    date_hierarchy = 'created_at'

