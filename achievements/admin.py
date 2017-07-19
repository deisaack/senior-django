from django.contrib import admin


from .models import (
	Question,
	Appraisal,
	Employee,
)

class QuestionInline(admin.TabularInline):
	model = Question
	extra = 0



class AppraisalAdmin(admin.ModelAdmin):
	inlines = [
		QuestionInline
	]
	# exclude=['question']

	class Meta:
		model = Appraisal


admin.site.register(Appraisal, AppraisalAdmin)

admin.site.register(Employee)

admin.site.register(Question)
