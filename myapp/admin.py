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
        'matric_number', 'email', 'faculty', 'department', 'level_of_study',
        'marital_status', 'mode_of_entry'
    )
    list_filter = (
        'faculty', 'department', 'level_of_study', 'sex', 'submission_date',
        'marital_status', 'mode_of_entry', 'nationality'
    )
    search_fields = (
        'firstname', 'surname', 'matric_number', 'submission_code', 'email',
        'jamb_reg_number', 'next_of_kin_name','department','faculty'
    )
    readonly_fields = ('submission_code', 'submission_date')
    actions = ["export_as_csv", "export_as_excel"]

    fieldsets = (
        ('Personal Information', {
            'fields': (
                'surname', 'firstname', 'othername', 'sex', 'date_of_birth',
                'marital_status', 'nationality', 'passport'
            )
        }),
        ('Contact Information', {
            'fields': (
                'email', 'phone_number', 'second_phone_number', 'whatsapp_name'
            )
        }),
        ('Academic Information', {
            'fields': (
                'faculty', 'department', 'level_of_study', 'matric_number',
                'mode_of_entry', 'jamb_reg_number'
            )
        }),
        ('Residential Information', {
            'fields': (
                'permanent_address', 'accommodation_type', 'residential_address',
                'state_of_residence', 'lga_of_residence'
            )
        }),
        ('Guardian & Next of Kin', {
            'fields': (
                'guardian_name', 'guardian_phone_number',
                'next_of_kin_name', 'next_of_kin_phone', 'next_of_kin_relationship'
            )
        }),
        ('Other Information', {
            'fields': (
                'religion', 'state_of_origin', 'local_government',
                'skills', 'extracurricular_activities'
            )
        }),
        ('System Information', {
            'fields': ('submission_code', 'submission_date'),
            'classes': ('collapse',)
        })
    )

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