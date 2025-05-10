import json
import csv
import xlsxwriter
from io import BytesIO

from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import StudentSubmission
from .serializers import StudentSubmissionSerializer

def generate_submission_code(matric_number):
    """
    Generate a unique submission code with prefix EMT followed by 
    the last 3 digits of the matric number.
    """
    # Extract the last 3 digits from the matric number
    digits = ''.join(filter(str.isdigit, matric_number))
    last_three_digits = digits[-3:] if len(digits) >= 3 else digits.zfill(3)
    
    code = f"EMT{last_three_digits}"
    
    # Check if this code already exists
    count = StudentSubmission.objects.filter(submission_code=code).count()
    if count > 0:
        # Append a suffix to make it unique
        return f"{code}{count}"
    
    return code

@api_view(['POST'])
@permission_classes([AllowAny])  # Add this line to allow unauthenticated access
def submit_form(request):
    """
    API endpoint for form submission.
    """
    serializer = StudentSubmissionSerializer(data=request.data)
    
    if serializer.is_valid():
        # Generate a unique submission code
        matric_number = request.data.get('matricNumber', '')
        submission_code = generate_submission_code(matric_number)
        
        # Save the instance with the generated code
        instance = serializer.save(submission_code=submission_code)
        
        return Response({
            'status': 'success',
            'message': 'Form submitted successfully',
            'code': submission_code
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'status': 'error',
        'message': 'Validation failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name='dispatch')
class StudentSubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and searching student submissions.
    """
    queryset = StudentSubmission.objects.all()
    serializer_class = StudentSubmissionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter queryset based on search parameters.
        """
        queryset = StudentSubmission.objects.all()
        search_query = self.request.query_params.get('search', None)
        
        if search_query:
            queryset = queryset.filter(
                Q(surname__icontains=search_query) |
                Q(firstname__icontains=search_query) |
                Q(matric_number__icontains=search_query) |
                Q(submission_code__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        
        return queryset

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_data(request):
    """
    Export all data in selected format (JSON, CSV, Excel).
    """
    format_type = request.GET.get('format', 'json')
    
    # Get all submissions
    submissions = StudentSubmission.objects.all()
    
    if format_type == 'json':
        # JSON export
        serializer = StudentSubmissionSerializer(submissions, many=True)
        data = serializer.data
        
        # Create a response with JSON data
        response = HttpResponse(json.dumps(data, indent=4), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="student_submissions.json"'
        
    elif format_type == 'csv':
        # CSV export
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="student_submissions.csv"'
        
        writer = csv.writer(response)
        
        # Write header row
        writer.writerow([
            'Submission Code', 'Submission Date', 'Surname', 'Firstname', 'Other Name',
            'Sex', 'Date of Birth', 'Email', 'Phone Number', 'WhatsApp Name',
            'Nationality', 'Faculty', 'Department', 'Level of Study', 'Matric Number',
            'Permanent Address', 'Accommodation Type', 'Residential Address',
            'State of Residence', 'LGA of Residence', 'Guardian Name',
            'Guardian Phone Number', 'Religion', 'State of Origin', 'Local Government',
            'Skills', 'Extracurricular Activities', 'Passport Image'
        ])
        
        # Write data rows
        for submission in submissions:
            writer.writerow([
                submission.submission_code,
                submission.submission_date,
                submission.surname,
                submission.firstname,
                submission.othername,
                submission.sex,
                submission.date_of_birth,
                submission.email,
                submission.phone_number,
                submission.whatsapp_name,
                submission.nationality,
                submission.faculty,
                submission.department,
                submission.level_of_study,
                submission.matric_number,
                submission.permanent_address,
                submission.accommodation_type,
                submission.residential_address,
                submission.state_of_residence,
                submission.lga_of_residence,
                submission.guardian_name,
                submission.guardian_phone_number,
                submission.religion,
                submission.state_of_origin,
                submission.local_government,
                submission.skills,
                submission.extracurricular_activities,
                request.build_absolute_uri(submission.passport.url) if submission.passport else ''
            ])
            
    elif format_type == 'excel':
        # Excel export
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'font_color': 'white',
            'bg_color': '#008000',  # Green
            'border': 1
        })
        
        row_format = workbook.add_format({
            'border': 1
        })
        
        # Write header row
        headers = [
            'Submission Code', 'Submission Date', 'Surname', 'Firstname', 'Other Name',
            'Sex', 'Date of Birth', 'Email', 'Phone Number', 'WhatsApp Name',
            'Nationality', 'Faculty', 'Department', 'Level of Study', 'Matric Number',
            'Permanent Address', 'Accommodation Type', 'Residential Address',
            'State of Residence', 'LGA of Residence', 'Guardian Name',
            'Guardian Phone Number', 'Religion', 'State of Origin', 'Local Government',
            'Skills', 'Extracurricular Activities', 'Passport Image'
        ]
        
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)
        
        # Write data rows
        for row_num, submission in enumerate(submissions, 1):
            row_data = [
                submission.submission_code,
                submission.submission_date.strftime('%Y-%m-%d %H:%M:%S'),
                submission.surname,
                submission.firstname,
                submission.othername,
                submission.sex,
                submission.date_of_birth.strftime('%Y-%m-%d'),
                submission.email,
                submission.phone_number,
                submission.whatsapp_name,
                submission.nationality,
                submission.faculty,
                submission.department,
                submission.level_of_study,
                submission.matric_number,
                submission.permanent_address,
                submission.accommodation_type,
                submission.residential_address,
                submission.state_of_residence,
                submission.lga_of_residence,
                submission.guardian_name,
                submission.guardian_phone_number,
                submission.religion,
                submission.state_of_origin,
                submission.local_government,
                submission.skills,
                submission.extracurricular_activities,
                request.build_absolute_uri(submission.passport.url) if submission.passport else ''
            ]
            
            for col_num, cell_data in enumerate(row_data):
                worksheet.write(row_num, col_num, cell_data, row_format)
        
        # Adjust column widths
        for col_num in range(len(headers)):
            worksheet.set_column(col_num, col_num, 15)
        
        workbook.close()
        
        # Create response with Excel file
        output.seek(0)
        response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="student_submissions.xlsx"'
        
    else:
        return Response({
            'status': 'error',
            'message': 'Invalid export format specified'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    return response