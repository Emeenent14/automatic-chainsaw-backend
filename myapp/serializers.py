from rest_framework import serializers
from .models import StudentSubmission

class StudentSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for the StudentSubmission model."""
    class Meta:
        model = StudentSubmission
        fields = '__all__'
        read_only_fields = ('submission_code', 'submission_date')

    def validate_phone_number(self, value):
        """
        Ensure phone number contains only digits.
        """
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value
    
    def validate_guardian_phone_number(self, value):
        """
        Ensure guardian phone number contains only digits.
        """
        if not value.isdigit():
            raise serializers.ValidationError("Guardian phone number must contain only digits.")
        return value
    
    def validate_matric_number(self, value):
        """
        Ensure matric number contains at least 3 digits.
        """
        if not any(char.isdigit() for char in value) or sum(c.isdigit() for c in value) < 3:
            raise serializers.ValidationError("Matric number must contain at least 3 digits.")
        return value
    
    def validate_passport(self, value):
        """
        Validate passport image file type.
        """
        if value:
            file_extension = value.name.split('.')[-1].lower()
            if file_extension not in ['jpg', 'jpeg', 'png']:
                raise serializers.ValidationError("Only JPG and PNG files are allowed.")
        return value
    
    # New validators:
    def validate_second_phone_number(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("Second phone number must contain only digits.")
        return value
    
    def validate_next_of_kin_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Next of kin phone number must contain only digits.")
        return value
    