from django import forms

from .models import Student


class StudentForm(forms.ModelForm):
    """Enrollment form used by the "Add student" modal."""

    GROUPS = (
        ("Personal information", ("first_name", "last_name", "date_of_birth", "phone", "email", "address")),
        ("Academic information", ("student_id", "program", "year_level", "section", "attendance", "enrolled_on", "status")),
        ("Background information", ("guardian_name", "guardian_phone", "previous_school", "notes")),
    )

    class Meta:
        model = Student
        fields = (
            "first_name", "last_name", "date_of_birth", "phone", "email", "address",
            "student_id", "program", "year_level", "section", "attendance", "enrolled_on", "status",
            "guardian_name", "guardian_phone", "previous_school", "notes",
        )
        labels = {
            "student_id": "Student ID",
            "year_level": "Year level",
            "attendance": "Attendance (%)",
            "date_of_birth": "Date of birth",
            "guardian_phone": "Guardian phone",
            "previous_school": "Previous school",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"autofocus": True}),
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "enrolled_on": forms.DateInput(attrs={"type": "date"}),
            "attendance": forms.NumberInput(attrs={"step": 1, "min": 0, "max": 100}),
            "address": forms.TextInput(attrs={"placeholder": "Street, city, province"}),
            "notes": forms.Textarea(attrs={"rows": 2, "placeholder": "Optional remarks"}),
        }

    def grouped_fields(self):
        for title, names in self.GROUPS:
            yield title, [self[name] for name in names]
