from django.contrib import admin
from django.http import HttpResponse
import csv
import xlsxwriter
from io import BytesIO
from .models import StudentSubmission

@admin.register(StudentSubmission)
class StudentSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'submission_code', 'submission_date', 'firstname', 'surname', 
        'matric_number', 'email', 'faculty', 'department', 'level_of_study'
    )
    list_filter = (
        'faculty', 'department', 'level_of_study', 'sex', 'submission_date',
    )
    search_fields = (
        'firstname', 'surname', 'matric_number', 'submission_code', 'email',
    )
    readonly_fields = ('submission_code', 'submission_date')

    actions = ["export_as_csv", "export_as_excel"]

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=student_submissions.csv"

        writer = csv.writer(response)
        headers = [field.name for field in StudentSubmission._meta.fields]
        writer.writerow(headers)

        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in headers])

        return response

    export_as_csv.short_description = "Export Selected to CSV"

    def export_as_excel(self, request, queryset):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet("Submissions")

        # Headers
        headers = [field.name for field in StudentSubmission._meta.fields]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        # Rows
        for row, obj in enumerate(queryset, start=1):
            for col, field in enumerate(headers):
                value = getattr(obj, field)
                if hasattr(value, 'strftime'):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                worksheet.write(row, col, str(value))

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=student_submissions.xlsx"
        return response

    export_as_excel.short_description = "Export Selected to Excel"
