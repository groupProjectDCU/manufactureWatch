from django import forms
from .models import FaultCase, FaultNote

class FaultCaseForm(forms.ModelForm):
    class Meta:
        model = FaultCase
        fields = ['machine', 'description', 'priority'] # Replace with the actual field names you want to include

    def __init__(self, *args, **kwargs): # Initialize the form
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items(): # Iterate over each field in the form
            field.widget.attrs['class'] = 'form-control' # Add Bootstrap class to each field's widget

class FaultNoteForm(forms.ModelForm):
    class Meta:
        model = FaultNote
        fields = ['case', 'note']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class FaultUpdateForm(forms.ModelForm):
    class Meta:
        model = FaultCase
        fields = ['status', 'priority', 'resolution_notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'