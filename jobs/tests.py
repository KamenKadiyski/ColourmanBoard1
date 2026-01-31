from django.test import TestCase
from django.db import IntegrityError, transaction

from jobs.models import Customer, Job
from labels.models import Label, LabelType, LabelSize


class JobAndCustomerModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create Label dependencies
        cls.size = LabelSize.objects.create(size="100x50", usage="General usage")
        cls.label_type = LabelType.objects.create(name="Standard", is_preprinted=False)
        cls.label_type.sizes.add(cls.size)
        cls.label = Label.objects.create(
            bar_code="1234567890",
            description="Test Label",
        )
        cls.label.label_types.add(cls.label_type)

        # Create Customer
        cls.customer = Customer.objects.create(name="Acme Corp")

        # Create Job
        cls.job = Job.objects.create(
            job_code="JOB-001",
            description="First job",
            customer=cls.customer,
        )
        cls.job.labels.add(cls.label)

    def test_customer_str_returns_name(self):
        self.assertEqual(str(self.customer), "Acme Corp")

    def test_customer_boolean_defaults_are_false(self):
        self.assertFalse(self.customer.only_preprinted_labels)
        self.assertFalse(self.customer.only_customer_colours)

    def test_job_str_returns_job_code(self):
        self.assertEqual(str(self.job), "JOB-001 - First job")

    def test_job_code_is_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Job.objects.create(
                    job_code="JOB-001",  # duplicate
                    description="Duplicate job",
                    customer=self.customer,
                )

    def test_deleting_customer_cascades_to_jobs(self):
        # Ensure the job exists first
        self.assertEqual(Job.objects.count(), 1)
        # Delete customer and verify cascading delete on jobs
        self.customer.delete()
        self.assertEqual(Job.objects.count(), 0)
