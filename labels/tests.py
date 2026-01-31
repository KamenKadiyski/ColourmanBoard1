from django.test import TestCase, Client
from django.urls import reverse
from labels.models import Label

class LabelsIndexTest(TestCase):
    def test_labels_index_empty(self):
        # Ensure no labels exist
        Label.objects.all().delete()
        client = Client()
        response = client.get(reverse('labels:labels_index'))
        self.assertEqual(response.status_code, 200)

    def test_labels_index_fewer_than_four(self):
        # Create fewer than 4 labels
        Label.objects.create(bar_code="123", description="Label 1")
        client = Client()
        response = client.get(reverse('labels:labels_index'))
        self.assertEqual(response.status_code, 200)
