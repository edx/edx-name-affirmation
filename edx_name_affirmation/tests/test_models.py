"""
Tests for Name Affirmation models
"""
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from edx_name_affirmation.models import VerifiedName
from edx_name_affirmation.statuses import VerifiedNameStatus

User = get_user_model()


def _obj(dictionary):
    "Helper method to turn a dict into an object. Used to mock below."

    return type('obj', (object,), dictionary)


class VerifiedNameModelTests(TestCase):
    """
    Test suite for the VerifiedName models
    """
    def setUp(self):
        self.verified_name = 'Test Tester'
        self.user = User.objects.create(username='modelTester', email='model@tester.com')
        self.verified_name = VerifiedName.objects.create(
            user=self.user,
            verified_name=self.verified_name,
            status=VerifiedNameStatus.SUBMITTED,
        )
        return super().setUp()

    @patch('edx_name_affirmation.models.SoftwareSecurePhotoVerification')
    def test_histories(self, sspv_mock):
        """
        Test the model history is recording records as expected
        """
        idv_attempt_id = 34455
        idv_attempt_status = 'submitted'

        sspv_mock.objects.get = lambda id: \
            _obj({'status': idv_attempt_status}) if id == idv_attempt_id \
            else _obj({'status': None})

        verified_name_history = self.verified_name.history.all().order_by('history_date')
        assert len(verified_name_history) == 1
        self.verified_name.status = VerifiedNameStatus.APPROVED
        self.verified_name.verification_attempt_id = idv_attempt_id

        assert self.verified_name.verification_attempt_status is idv_attempt_status
        self.verified_name.save()
        verified_name_history = self.verified_name.history.all().order_by('history_date')
        assert len(verified_name_history) == 2

        first_history_record = verified_name_history[0]
        assert first_history_record.status == VerifiedNameStatus.SUBMITTED
        assert first_history_record.verification_attempt_id is None

        second_history_record = verified_name_history[1]
        assert second_history_record.status == VerifiedNameStatus.APPROVED
        assert second_history_record.verification_attempt_id == idv_attempt_id
