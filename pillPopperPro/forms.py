from django import forms
from pillPopperPro.models import Pill

class PillForm(forms.Form):
    class Meta:
        model = Pill
        fields = ('name', 'dosage', 'disposal_time', 'quantity_initial')

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 200:
            raise forms.ValidationError('Prescription name is too long')
        if not name or len(name) == 0:
            raise forms.ValidationError('Including a prescription name is requred')
        return name

    def clean_dosage(self):
        dosage = self.cleaned_data['dosage']
        if dosage < 1 or dosage > 9999:
            raise forms.ValidationError('Please re-enter a valid dosage')
        return dosage

    def clean_quantity_initial(self):
        quantity_initial = self.cleaned_data['quantity_initial']
        if quantity_initial != 30: # only accepting a 30 day supply
            raise forms.ValidationError('Please enter valid quantity')
        return quantity_initial