from urllib.parse import urlencode

from django.db.models import Avg, Count, Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import StudentForm
from .models import Student
from .search import fuzzy_match


def student_list(request):
    """Class list with fuzzy live search, a modal profile and an enrollment form."""
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect(f"{reverse('student-list')}?student={student.pk}")
    else:
        form = StudentForm(
            initial={
                "enrolled_on": timezone.localdate(),
                "status": Student.Status.ACTIVE,
                "attendance": 100,
            }
        )

    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")

    students = list(Student.objects.all())
    if q:
        students = [s for s in students if fuzzy_match(q, s.search_text)]
    if status in dict(Student.Status.choices):
        students = [s for s in students if s.status == status]

    if request.GET.get("rows"):
        response = render(request, "students/_rows.html", {"students": students})
        response["X-Result-Count"] = str(len(students))
        return response

    sid = request.GET.get("student", "")
    selected = next((s for s in students if str(s.pk) == sid), None) if sid.isdigit() else None

    if request.GET.get("partial"):
        if not selected:
            raise Http404
        return render(request, "students/_profile.html", {"s": selected})

    params = {k: v for k, v in (("q", q), ("status", status)) if v}
    totals = Student.objects.aggregate(
        total=Count("pk"),
        active=Count("pk", filter=Q(status=Student.Status.ACTIVE)),
        avg_attendance=Avg("attendance"),
    )

    return render(
        request,
        "students/list.html",
        {
            "students": students,
            "selected": selected,
            "q": q,
            "status": status,
            "query": urlencode(params),
            "add_form": form,
            "show_add": request.method == "POST" and not form.is_valid(),
            "stats": {
                **totals,
                "inactive": totals["total"] - totals["active"],
                "programs": Student.objects.values("program").distinct().count(),
            },
        },
    )
