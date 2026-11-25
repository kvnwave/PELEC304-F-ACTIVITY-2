from django.core.management.base import BaseCommand

from students.models import Student

STUDENTS = [
    dict(student_id="2024-0001", first_name="Maria Clara", last_name="Santos", email="mc.santos@example.com",
         phone="0917 555 0101", date_of_birth="2005-03-14", address="12 Mabini St., Imus, Cavite",
         guardian_name="Elena Santos", guardian_phone="0918 555 0201", previous_school="Imus National High School",
         program="BS Information Technology", year_level=2, section="A", attendance=100,
         enrolled_on="2024-08-05", status="active",
         notes="Dean's Lister, 1st Semester AY 2025-2026. Active member of the IT Society."),
    dict(student_id="2024-0002", first_name="Jose Miguel", last_name="Dela Cruz", email="jm.delacruz@example.com",
         phone="0917 555 0102", date_of_birth="2004-11-02", address="88 Rizal Ave., Bacoor, Cavite",
         guardian_name="Ramon Dela Cruz", guardian_phone="0918 555 0202", previous_school="Bacoor National High School",
         program="BS Computer Science", year_level=3, section="B", attendance=96,
         enrolled_on="2024-08-05", status="active",
         notes="Team lead, capstone project on campus navigation."),
    dict(student_id="2024-0003", first_name="Andrea", last_name="Villanueva", email="a.villanueva@example.com",
         phone="0917 555 0103", date_of_birth="2005-07-21", address="5 Katipunan St., Dasmarinas, Cavite",
         guardian_name="Lorna Villanueva", guardian_phone="0918 555 0203", previous_school="Dasmarinas National High School",
         program="BS Accountancy", year_level=2, section="C", attendance=100,
         enrolled_on="2024-08-05", status="active", notes="Consistent top three of the batch."),
    dict(student_id="2024-0004", first_name="Nathaniel", last_name="Bautista", email="n.bautista@example.com",
         phone="0917 555 0104", date_of_birth="2004-01-09", address="31 Aguinaldo Hwy., Silang, Cavite",
         guardian_name="Ferdinand Bautista", guardian_phone="0918 555 0204", previous_school="Silang National High School",
         program="BS Civil Engineering", year_level=4, section="A", attendance=92,
         enrolled_on="2024-08-05", status="active", notes="OJT completed at Cavite Public Works Office."),
    dict(student_id="2024-0005", first_name="Bea Kristine", last_name="Ramos", email="bk.ramos@example.com",
         phone="0917 555 0105", date_of_birth="2005-05-30", address="19 Tirona St., Kawit, Cavite",
         guardian_name="Marites Ramos", guardian_phone="0918 555 0205", previous_school="Kawit National High School",
         program="BS Nursing", year_level=2, section="B", attendance=98,
         enrolled_on="2024-08-05", status="active", notes="Volunteer, community health outreach program."),
    dict(student_id="2024-0006", first_name="Gabriel", last_name="Mendoza", email="g.mendoza@example.com",
         phone="0917 555 0106", date_of_birth="2003-09-18", address="64 Molino Blvd., Bacoor, Cavite",
         guardian_name="Arturo Mendoza", guardian_phone="0918 555 0206", previous_school="Molino National High School",
         program="BS Information Technology", year_level=4, section="A", attendance=88,
         enrolled_on="2024-08-05", status="active", notes="Freelance web developer while studying."),
    dict(student_id="2024-0007", first_name="Liza", last_name="Aquino", email="l.aquino@example.com",
         phone="0917 555 0107", date_of_birth="2005-12-05", address="7 Salawag Rd., Dasmarinas, Cavite",
         guardian_name="Nora Aquino", guardian_phone="0918 555 0207", previous_school="Salawag National High School",
         program="BS Accountancy", year_level=1, section="C", attendance=100,
         enrolled_on="2024-08-05", status="active", notes="Enrolled late; attendance is monitored weekly."),
    dict(student_id="2024-0008", first_name="Marco", last_name="Fernandez", email="m.fernandez@example.com",
         phone="0917 555 0108", date_of_birth="2003-02-26", address="102 Anabu Rd., Imus, Cavite",
         guardian_name="Roberto Fernandez", guardian_phone="0918 555 0208", previous_school="Anabu National High School",
         program="BS Computer Science", year_level=3, section="B", attendance=74,
         enrolled_on="2024-08-05", status="inactive",
         notes="Leave of absence requested for the current semester."),
]


class Command(BaseCommand):
    help = "Create or update the sample enrollment records."

    def handle(self, *args, **options):
        for row in STUDENTS:
            Student.objects.update_or_create(student_id=row["student_id"], defaults=row)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(STUDENTS)} students."))
