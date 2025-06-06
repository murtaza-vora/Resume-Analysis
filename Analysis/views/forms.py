from django import forms

from Analysis.models import Candidate


class CandidateForm(forms.Form):
    csv_file = forms.FileField()



class CandidateResumeForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'
