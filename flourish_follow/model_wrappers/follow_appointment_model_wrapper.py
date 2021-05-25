from django.conf import settings
from dateutil.relativedelta import relativedelta

from edc_model_wrapper import ModelWrapper
from flourish_caregiver.models import SubjectConsent
from .consent_model_wrapper_mixin import ConsentModelWrapperMixin


class FollowAppointmentModelWrapper(ConsentModelWrapperMixin, ModelWrapper):

    model = 'edc_appointment.appointment'
    querystring_attrs = ['subject_identifier']
    next_url_attrs = ['study_maternal_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'flourish_follow_appt_listboard_url')

    @property
    def subject_consent(self):
        """Returns a subject consent object.
        """
        return SubjectConsent.objects.filter(
            subject_identifier=self.object.subject_identifier).last()

    @property
    def gender(self):
        """Returns the gender of the participant.
        """
        return self.subject_consent.gender

    @property
    def first_name(self):
        """Returns the participant's first name.
        """
        return self.subject_consent.first_name

    @property
    def last_name(self):
        """Returns the participant's last name.
        """
        return self.subject_consent.last_name

    @property
    def earliesr_date_due(self):
        """Returns the earlist date to see a participant.
        """
        return self.object.appt_datetime - relativedelta(days=45)

    @property
    def latest_date_due(self):
        """Returns the last date to see a participant.
        """
        return self.object.appt_datetime + relativedelta(days=45)

    @property
    def ideal_date_due(self):
        """Ideal date due to see a participant.
        """
        return self.earliesr_date_due + (
            self.latest_date_due - self.earliesr_date_due)/2
