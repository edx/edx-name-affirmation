"""Defines serializers used by the Name Affirmation API"""

import re

from rest_framework import serializers

from django.contrib.auth import get_user_model

from edx_name_affirmation.models import VerifiedName, VerifiedNameConfig

User = get_user_model()


class VerifiedNameSerializer(serializers.ModelSerializer):
    """
    Serializer for the VerifiedName Model.
    """
    username = serializers.CharField(source="user.username")
    verified_name = serializers.CharField(required=True)
    profile_name = serializers.CharField(required=True)
    verification_attempt_id = serializers.IntegerField(required=False, allow_null=True)
    verification_attempt_status = serializers.SerializerMethodField('get_verification_attempt_status')
    proctored_exam_attempt_id = serializers.IntegerField(required=False, allow_null=True)
    status = serializers.CharField(required=False, allow_null=True)

    def get_verification_attempt_status(self, obj):
        try:
            from lms.djangoapps.verify_student.services import IDVerificationService # pylint: disable=import-error,import-outside-toplevel
        except ImportError:
            return None

        idv_attempt_id = obj.verification_attempt_id

        if not idv_attempt_id:
            return None

        verification = IDVerificationService.get_verification_details_by_id(idv_attempt_id)

        return verification.status if verification else None

    class Meta:
        """
        Meta Class
        """
        model = VerifiedName

        fields = (
            "id", "created", "username", "verified_name", "profile_name", "verification_attempt_id",
            "verification_attempt_status", "proctored_exam_attempt_id", "status"
        )

    def validate_verified_name(self, verified_name):
        if self._contains_html(verified_name):
            raise serializers.ValidationError('Name cannot contain the following characters: < >')
        if self._contains_url(verified_name):
            raise serializers.ValidationError('Name cannot contain a URL')

    def _contains_html(self, string):
        """
        Validator method to check whether a string contains HTML tags
        """
        regex = re.compile('(<|>)', re.UNICODE)
        return bool(regex.search(string))

    def _contains_url(self, string):
        """
        Validator method to check whether a string contains a url
        """
        regex = re.findall(r'https|http?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', string)
        return bool(regex)


class UpdateVerifiedNameSerializer(VerifiedNameSerializer):
    """
    Serializer for updates to the VerifiedName Model.
    """
    username = serializers.CharField(source='user.username', required=True)
    verified_name = serializers.CharField(required=False)
    profile_name = serializers.CharField(required=False)
    status = serializers.CharField(required=True)


class VerifiedNameConfigSerializer(serializers.ModelSerializer):
    """
    Serializer for the VerifiedNameConfig Model.
    """
    username = serializers.CharField(source="user.username")
    use_verified_name_for_certs = serializers.BooleanField(required=False, allow_null=True)

    class Meta:
        """
        Meta Class
        """
        model = VerifiedNameConfig

        fields = ("change_date", "username", "use_verified_name_for_certs")
