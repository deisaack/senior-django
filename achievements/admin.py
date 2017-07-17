from django.contrib import admin


from .models import (
	Question,
	Appraisal,
	Superior
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


# admin.site.register(Appraisal, AppraisalAdmin)
admin.site.register(Appraisal)
admin.site.register(Question)
admin.site.register(Superior)

