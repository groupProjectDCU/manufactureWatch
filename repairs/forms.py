from django import forms
from .models import FaultCase, FaultNote

class FaultCaseForm(forms.ModelForm):
    class Meta:
        model = FaultCase
        fields = ['machine', 'description', 'priority']

class FaultNoteForm(forms.ModelForm):
    class Meta:
        model = FaultNote
        fields = ['case', 'note']

class FaultUpdateForm(forms.ModelForm):
    class Meta:
        model = FaultCase
        fields = ['status', 'priority', 'resolution_notes']