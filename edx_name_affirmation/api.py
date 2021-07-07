"""
Python API for edx_name_affirmation.
"""

import logging

from edx_name_affirmation.exceptions import (
    VerifiedNameAttemptIdNotGiven,
    VerifiedNameDoesNotExist,
    VerifiedNameEmptyString,
    VerifiedNameMultipleAttemptIds
)
from edx_name_affirmation.models import VerifiedName

log = logging.getLogger(__name__)


def create_verified_name(
    user, verified_name, profile_name, verification_attempt_id=None,
    proctored_exam_attempt_id=None, is_verified=False,
):
    """
    Create a new `VerifiedName` for the given user.

    Arguments:
        * `user` (User object)
        * `verified_name` (str): Representative of the name on the user's physical ID card.
        * `profile_name` (str): A snapshot of either 1) the user's pending name change if given
          or 2) the existing name on the user's profile.
        * `verification_attempt_id` (int): Optional reference to an external ID verification
          attempt.
        * `proctored_exam_attempt_id` (int): Optional reference to an external proctored exam
          attempt.
        * `is_verified` (bool): Optional, defaults False. This should determine whether the
          verified_name is valid for use with ID verification, exams, etc.
    """
    # Do not allow empty strings
    if verified_name == '':
        raise VerifiedNameEmptyString('verified_name', user.id)
    if profile_name == '':
        raise VerifiedNameEmptyString('profile_name', user.id)

    # Only link to one attempt
    if verification_attempt_id and proctored_exam_attempt_id:
        err_msg = (
            'Attempted to create VerifiedName for user_id={user_id}, but two different '
            'external attempt IDs were given. Only one may be used. '
            'verification_attempt_id={verification_attempt_id}, '
            'proctored_exam_attempt_id={proctored_exam_attempt_id}, '
            'is_verified={is_verified}'.format(
                user_id=user.id, verification_attempt_id=verification_attempt_id,
                proctored_exam_attempt_id=proctored_exam_attempt_id, is_verified=is_verified,
            )
        )
        raise VerifiedNameMultipleAttemptIds(err_msg)

    VerifiedName.objects.create(
        user=user,
        verified_name=verified_name,
        profile_name=profile_name,
        verification_attempt_id=verification_attempt_id,
        proctored_exam_attempt_id=proctored_exam_attempt_id,
        is_verified=is_verified,
    )

    log_msg = (
        'VerifiedName created for user_id={user_id}. '
        'verification_attempt_id={verification_attempt_id}, '
        'proctored_exam_attempt_id={proctored_exam_attempt_id}, '
        'is_verified={is_verified}'.format(
            user_id=user.id, verification_attempt_id=verification_attempt_id,
            proctored_exam_attempt_id=proctored_exam_attempt_id, is_verified=is_verified,
        )
    )
    log.info(log_msg)


def get_verified_name(user, is_verified=False):
    """
    Get the most recent VerifiedName for a given user.

    Arguments:
        * `user` (User object)
        * `is_verified` (bool): Optional, set to True to ignore entries that are not
          verified.

    Returns a VerifiedName object.
    """
    verified_name_qs = VerifiedName.objects.filter(user=user).order_by('-created')

    if is_verified:
        return verified_name_qs.filter(is_verified=True).first()

    return verified_name_qs.first()


def update_verification_attempt_id(user, verification_attempt_id):
    """
    Update the `verification_attempt_id` for the user's most recent VerifiedName.

    If the VerifiedName already has a linked verification or proctored exam attempt, create a new
    VerifiedName instead, using the same `verified_name` and `profile_name`.

    This will raise an exception if the user does not have an existing VerifiedName.

    Arguments:
        * `user` (User object)
        * `verification_attempt_id` (int)
    """
    verified_name_obj = get_verified_name(user)

    if not verified_name_obj:
        err_msg = (
            'Attempted to update most recent VerifiedName for user_id={user_id} with '
            'verification_attempt_id={verification_attempt_id}, but this user does not have '
            'an existing VerifiedName.'.format(
                user_id=user.id, verification_attempt_id=verification_attempt_id
            )
        )
        raise VerifiedNameDoesNotExist(err_msg)

    if verified_name_obj.verification_attempt_id or verified_name_obj.proctored_exam_attempt_id:
        log_msg = (
            'Attempted to update VerifiedName id={id} with '
            'verification_attempt_id={verification_attempt_id}, but it already has a linked attempt. '
            'Creating a new VerifiedName for user_id={user_id}'.format(
                id=verified_name_obj.id, verification_attempt_id=verification_attempt_id, user_id=user.id,
            )
        )
        log.warning(log_msg)

        create_verified_name(
            user=user,
            verified_name=verified_name_obj.verified_name,
            profile_name=verified_name_obj.profile_name,
            verification_attempt_id=verification_attempt_id,
        )

    verified_name_obj.verification_attempt_id = verification_attempt_id
    verified_name_obj.save()

    log_msg = (
        'Updated VerifiedName id={id} with verification_attempt_id={verification_attempt_id} '
        'for user_id={user_id}'.format(
            id=verified_name_obj.id, verification_attempt_id=verification_attempt_id, user_id=user.id,
        )
    )
    log.info(log_msg)


def update_is_verified_status(
    user, is_verified, verification_attempt_id=None, proctored_exam_attempt_id=None
):
    """
    Update the status of a VerifiedName using the linked ID verification or exam attempt ID. Only one
    of these should be specified.

    Arguments:
        * user (User object)
        * is_verified (bool)
        * verification_attempt_id (int)
        * proctored_exam_attempt_id (int)
    """
    filters = {'user': user}

    if verification_attempt_id:
        if proctored_exam_attempt_id:
            err_msg = (
                'Attempted to update the is_verified status for a VerifiedName, but two different '
                'attempt IDs were given. verification_attempt_id={verification_attempt_id}, '
                'proctored_exam_attempt_id={proctored_exam_attempt_id}'.format(
                    verification_attempt_id=verification_attempt_id,
                    proctored_exam_attempt_id=proctored_exam_attempt_id,
                )
            )
            raise VerifiedNameMultipleAttemptIds(err_msg)
        filters['verification_attempt_id'] = verification_attempt_id
    elif proctored_exam_attempt_id:
        filters['proctored_exam_attempt_id'] = proctored_exam_attempt_id
    else:
        err_msg = (
            'Attempted to update the is_verified status for a VerifiedName, but no '
            'verification_attempt_id or proctored_exam_attempt_id was given.'
        )
        raise VerifiedNameAttemptIdNotGiven(err_msg)

    verified_name_obj = VerifiedName.objects.filter(**filters).order_by('-created').first()

    if not verified_name_obj:
        err_msg = (
            'Attempted to update is_verified={is_verified} for a VerifiedName, but one does '
            'not exist for the given attempt ID. verification_attempt_id={verification_attempt_id}, '
            'proctored_exam_attempt_id={proctored_exam_attempt_id}'.format(
                is_verified=is_verified,
                verification_attempt_id=verification_attempt_id,
                proctored_exam_attempt_id=proctored_exam_attempt_id,
            )
        )
        raise VerifiedNameDoesNotExist(err_msg)

    verified_name_obj.is_verified = is_verified
    verified_name_obj.save()

    log_msg = (
        'Updated is_verified={is_verified} for VerifiedName belonging to user_id={user_id}. '
        'verification_attempt_id={verification_attempt_id}, '
        'proctored_exam_attempt_id={proctored_exam_attempt_id}'.format(
            is_verified=is_verified,
            user_id=verified_name_obj.user.id,
            verification_attempt_id=verification_attempt_id,
            proctored_exam_attempt_id=proctored_exam_attempt_id,
        )
    )
    log.info(log_msg)


def _edit_distance(old_name, new_name):
    """
    Return number of edits needed to transform one string into the other
    """
    if len(old_name) == 0:
        return len(new_name)

    if len(new_name) == 0:
        return len(old_name)

    if old_name[-1] == new_name[-1]:
        return _edit_distance(old_name[:-1], new_name[:-1])

    return 1 + min(
        _edit_distance(old_name, new_name[:-1]),  # insert
        _edit_distance(old_name[:-1], new_name),  # remove
        _edit_distance(old_name[:-1], new_name[:-1])  # replace
    )

def _added_space_valid(old_name, new_name):
    """
    Return true if added spaces are valid
    """

    # check that no more than 2 spaces have been added or removed
    old_space_count = old_name.count(' ')
    new_space_count = new_name.count(' ')
    diff_count = abs(old_space_count - new_space_count)
    if diff_count > 2:
        return False

    # check that added spaces occur in a valid place (i.e. cannot have two spaces in a row)
    old_splits = old_name.split()
    new_splits = new_name.split()
    diff_splits = abs(len(old_splits) - len(new_splits))
    if diff_count != diff_splits:
        return False

    return True

def are_name_edits_valid(old_name, new_name):
    """
    Return true if new name contains only valid edits, false otherwise
    Valid edits include one character change (insert/replace/remove) and the addition of at most two spaces
    """
    # check edits without spaces
    edits = _edit_distance(old_name.replace(" ", ""), new_name.replace(" ", ""))
    if edits > 1:
        return False

    # check that any addition of spaces is valid
    spaces_valid = _added_space_valid(old_name, new_name)
    return spaces_valid
