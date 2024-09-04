"""
Tests for Name Affirmation models
"""
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from edx_name_affirmation.models import VerifiedName
from edx_name_affirmation.statuses import VerifiedNameStatus

User = get_user_model()

idv_attempt_id = 34455
idv_attempt_status = 'submitted'

idv_attempt_id_notfound = 404
idv_attempt_id_notfound_status = None


def _obj(dictionary):
    "Helper method to turn a dict into an object. Used to mock below."

    return type('obj', (object,), dictionary)


def _mocked_model_get(id):  # pylint: disable=redefined-builtin
    "Helper method to mock the behavior of SoftwareSecurePhotoVerification model. Used to mock below."
    if id == idv_attempt_id_notfound:
        raise ObjectDoesNotExist

    if id == idv_attempt_id:
        return _obj({'status': idv_attempt_status})

    return _obj({'status': None})


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

    def test_histories(self):
        """
        Test the model history is recording records as expected
        """

        verified_name_history = self.verified_name.history.all().order_by('history_date')
        assert len(verified_name_history) == 1
        self.verified_name.status = VerifiedNameStatus.APPROVED
        self.verified_name.verification_attempt_id = idv_attempt_id
        self.verified_name.save()
        verified_name_history = self.verified_name.history.all().order_by('history_date')
        assert len(verified_name_history) == 2

        first_history_record = verified_name_history[0]
        assert first_history_record.status == VerifiedNameStatus.SUBMITTED
        assert first_history_record.verification_attempt_id is None

        second_history_record = verified_name_history[1]
        assert second_history_record.status == VerifiedNameStatus.APPROVED
        assert second_history_record.verification_attempt_id == idv_attempt_id

    @patch('edx_name_affirmation.models.SoftwareSecurePhotoVerification')
    def test_verification_status(self, sspv_mock):
        """
        Test the model history is recording records as expected
        """
        sspv_mock.objects.get = _mocked_model_get

        self.verified_name.verification_attempt_id = idv_attempt_id_notfound
        assert self.verified_name.verification_attempt_status is idv_attempt_id_notfound_status

        self.verified_name.verification_attempt_id = idv_attempt_id
        assert self.verified_name.verification_attempt_status is idv_attempt_status
