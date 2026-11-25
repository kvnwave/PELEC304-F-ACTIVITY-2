from django.test import TestCase
from django.urls import reverse

from .models import Student


class ProfileViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ana = Student.objects.create(
            student_id="2024-0001", first_name="Ana", last_name="Reyes",
            email="ana.reyes@example.com", program="BS Information Technology",
            year_level=1, section="A", attendance=100, enrolled_on="2024-08-05",
        )
        cls.ben = Student.objects.create(
            student_id="2024-0002", first_name="Ben", last_name="Cruz",
            email="ben.cruz@example.com", program="BS Computer Science",
            year_level=2, section="B", attendance=80, enrolled_on="2024-08-05",
        )

    def test_list_shows_every_student(self):
        response = self.client.get(reverse("student-list"))
        self.assertContains(response, "Ana Reyes")
        self.assertContains(response, "Ben Cruz")

    def test_selected_student_profile_is_rendered_in_modal(self):
        response = self.client.get(reverse("student-list"), {"student": self.ben.pk})
        self.assertEqual(response.context["selected"], self.ben)
        self.assertContains(response, "ben.cruz@example.com")
        self.assertContains(response, 'class="modal open"')

    def test_profile_fragment_for_modal(self):
        response = self.client.get(
            reverse("student-list"), {"student": self.ben.pk, "partial": "1"}
        )
        self.assertContains(response, "ben.cruz@example.com")
        self.assertNotContains(response, "<html")

    def test_profile_fragment_requires_a_student(self):
        response = self.client.get(reverse("student-list"), {"partial": "1"})
        self.assertEqual(response.status_code, 404)

    def test_fuzzy_search_tolerates_typos(self):
        response = self.client.get(reverse("student-list"), {"q": "Ana Reyz"})
        self.assertContains(response, "Ana Reyes")
        self.assertNotContains(response, "Ben Cruz")

    def test_fuzzy_search_matches_partial_words(self):
        response = self.client.get(reverse("student-list"), {"q": "comp sci"})
        self.assertContains(response, "Ben Cruz")
        self.assertNotContains(response, "Ana Reyes")

    def test_fuzzy_search_rejects_unrelated_text(self):
        response = self.client.get(reverse("student-list"), {"q": "zzzz"})
        self.assertEqual(response.context["students"], [])

    def test_live_rows_fragment(self):
        response = self.client.get(reverse("student-list"), {"rows": "1", "q": "Benn"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ben Cruz")
        self.assertNotContains(response, "<html")
        self.assertEqual(response["X-Result-Count"], "1")

    def test_grid_and_list_view_switch_is_present(self):
        response = self.client.get(reverse("student-list"))
        self.assertContains(response, 'data-view="grid"')
        self.assertContains(response, 'data-view="list"')
        self.assertContains(response, "student-table")
        self.assertContains(response, 'aria-label="Card view"')
        self.assertContains(response, 'aria-label="List view"')

    def test_attendance_help_text_is_rendered_with_its_id(self):
        response = self.client.get(reverse("student-list"))
        self.assertContains(response, 'id="id_attendance_helptext"')
        self.assertContains(response, 'aria-describedby="id_attendance_helptext"')

    def test_year_level_out_of_range_is_rejected(self):
        for value in ("0", "7"):
            response = self.client.post(
                reverse("student-list"),
                {
                    "first_name": "Test", "last_name": "Enrollee",
                    "student_id": f"2024-90{value}", "email": f"t{value}@example.com",
                    "program": "BS Nursing", "year_level": value,
                    "attendance": "90", "enrolled_on": "2024-08-05", "status": "active",
                },
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn("year_level", response.context["add_form"].errors)
        self.assertEqual(Student.objects.count(), 2)

    def test_year_label_covers_first_to_sixth(self):
        student = Student(year_level=6)
        self.assertEqual(student.year_label, "6th Year")
        student.year_level = 0
        self.assertEqual(student.year_label, "1st Year")

    def test_attendance_above_one_hundred_is_rejected(self):
        response = self.client.post(
            reverse("student-list"),
            {
                "first_name": "Test", "last_name": "Enrollee",
                "student_id": "2024-9500", "email": "t150@example.com",
                "program": "BS Nursing", "year_level": "1",
                "attendance": "150", "enrolled_on": "2024-08-05", "status": "active",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("attendance", response.context["add_form"].errors)

    def test_attendance_is_shown_as_a_percentage(self):
        response = self.client.get(reverse("student-list"))
        self.assertContains(response, "100%")
        self.assertContains(response, "80%")

    def test_average_attendance_stat(self):
        response = self.client.get(reverse("student-list"))
        self.assertContains(response, "90%")

    def test_search_narrows_the_list(self):
        response = self.client.get(reverse("student-list"), {"q": "Computer"})
        self.assertContains(response, "Ben Cruz")
        self.assertNotContains(response, "Ana Reyes")

    def test_status_filter(self):
        response = self.client.get(reverse("student-list"), {"status": "inactive"})
        self.assertEqual(response.context["students"], [])

    def test_unknown_student_is_ignored(self):
        response = self.client.get(reverse("student-list"), {"student": "9999"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["selected"])

    def test_add_student_button_is_present(self):
        response = self.client.get(reverse("student-list"))
        self.assertContains(response, "Add student")
        self.assertContains(response, 'data-open="add-modal"')

    def test_add_student_creates_record_and_opens_profile(self):
        response = self.client.post(
            reverse("student-list"),
            {
                "first_name": "Carla", "last_name": "Dizon", "student_id": "2024-0009",
                "email": "carla.dizon@example.com", "program": "BS Nursing",
                "year_level": "1", "section": "A", "attendance": "95",
                "enrolled_on": "2024-08-05", "status": "active",
            },
        )
        student = Student.objects.get(student_id="2024-0009")
        self.assertRedirects(response, f"{reverse('student-list')}?student={student.pk}")
        self.assertEqual(student.full_name, "Carla Dizon")
        self.assertEqual(student.attendance, 95)

    def test_invalid_add_student_reopens_form_with_errors(self):
        response = self.client.post(reverse("student-list"), {"first_name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["show_add"])
        self.assertTrue(response.context["add_form"].errors)
        self.assertContains(response, 'class="modal open"')
        self.assertEqual(Student.objects.count(), 2)

    def test_empty_class_renders(self):
        Student.objects.all().delete()
        response = self.client.get(reverse("student-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["selected"])
