from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Student(models.Model):
    """A single enrollee, holding personal, background and academic details."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    student_id = models.CharField(max_length=12, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)

    # Personal
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=160, blank=True)

    # Background
    guardian_name = models.CharField(max_length=120, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True)
    previous_school = models.CharField(max_length=120, blank=True)

    # Academic
    program = models.CharField(max_length=80)
    year_level = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
    )
    section = models.CharField(max_length=20, blank=True)
    attendance = models.PositiveSmallIntegerField(
        default=100,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Attendance percentage; 100 means no absences.",
    )
    enrolled_on = models.DateField()
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.ACTIVE)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("last_name", "first_name")

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def initials(self):
        return f"{self.first_name[:1]}{self.last_name[:1]}".upper()

    @property
    def year_label(self):
        labels = ("1st", "2nd", "3rd", "4th", "5th", "6th")
        return f"{labels[max(1, min(self.year_level, len(labels))) - 1]} Year"

    @property
    def search_text(self):
        """Everything the search box may look at, in one lowercase string."""
        return " ".join(
            str(part)
            for part in (
                self.full_name, self.student_id, self.email, self.phone,
                self.program, self.section, f"year {self.year_level}",
                self.get_status_display(), self.previous_school,
            )
            if part
        ).lower()

    @property
    def attendance_tone(self):
        if self.attendance >= 95:
            return "high"
        return "mid" if self.attendance >= 85 else "low"

    @property
    def tone(self):
        """Stable pastel index for the avatar tile."""
        return sum(map(ord, self.student_id)) % 5
