from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "full_name", "program", "year_level", "section", "status")
    list_filter = ("status", "program", "year_level")
    search_fields = ("student_id", "first_name", "last_name", "email")
