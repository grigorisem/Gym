from django.contrib import admin
from .models import Enrollment, MembershipPlan

# Register your models here.
admin.site.register(Enrollment)
admin.site.register(MembershipPlan)