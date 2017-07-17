from django import forms


from .models import Question, Employee, Appraisal

class ReviewForm(forms.ModelForm):
	question = forms.CharField(
		widget=forms.TextInput(attrs={'class': 'form-control'}),
		max_length=50,
		required=False)

	class Meta:
		model = Appraisal
		fields = ['employee']
