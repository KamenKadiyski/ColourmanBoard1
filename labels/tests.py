from django.test import TestCase, Client
from django.urls import reverse
from labels.models import Label


class LabelsIndexTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_labels_index_empty(self):
        # Ensure no labels exist
        Label.objects.all().delete()
        response = self.client.get(reverse('labels:labels_index'))
        self.assertEqual(response.status_code, 200)
        # context should always include last_labels list
        self.assertIn('last_labels', response.context)
        self.assertEqual(list(response.context['last_labels']), [])

    def test_labels_index_fewer_than_four(self):
        # Create fewer than 4 labels
        Label.objects.create(bar_code="123", description="Label 1")
        response = self.client.get(reverse('labels:labels_index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('last_labels', response.context)
        self.assertLessEqual(len(response.context['last_labels']), 3)

    def test_labels_index_shows_most_recent_three(self):
        # Create more than 3 labels and ensure slicing returns 3 most recent
        for i in range(5):
            Label.objects.create(bar_code=f"{100+i}", description=f"L{i}")
        response = self.client.get(reverse('labels:labels_index'))
        self.assertEqual(response.status_code, 200)
        last_labels = list(response.context['last_labels'])
        self.assertEqual(len(last_labels), 3)
        # Ensure ordering by -id (most recent first)
        self.assertTrue(all(last_labels[i].id > last_labels[i+1].id for i in range(2)))


class LabelsListTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_labels_list_default_orders_desc(self):
        l1 = Label.objects.create(bar_code="111", description="Alpha")
        l2 = Label.objects.create(bar_code="222", description="Beta")
        response = self.client.get(reverse('labels:labels_list'))
        self.assertEqual(response.status_code, 200)
        listed = list(response.context['last_labels'])
        # ordered by -id => l2 first
        self.assertEqual(listed[0], l2)
        self.assertEqual(listed[1], l1)

    def test_labels_list_filters_by_description(self):
        l1 = Label.objects.create(bar_code="111", description="Red Box")
        l2 = Label.objects.create(bar_code="222", description="Blue Crate")
        # Search by partial description
        response = self.client.get(reverse('labels:labels_list'), { 'search_term': 'Red' })
        self.assertEqual(response.status_code, 200)
        results = list(response.context['last_labels'])
        self.assertIn(l1, results)
        self.assertNotIn(l2, results)


class LabelDetailsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_label_details_renders_context(self):
        label = Label.objects.create(bar_code='777', description='Detail')
        response = self.client.get(reverse('labels:label_details', args=[label.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['label'].id, label.id)
        self.assertEqual(response.context['page_title'], label.description)

    def test_label_details_not_found_returns_404(self):
        response = self.client.get(reverse('labels:label_details', args=[99999]))
        self.assertEqual(response.status_code, 404)


class LabelCreateEditViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_add_label_get_renders_form(self):
        response = self.client.get(reverse('labels:add_label'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_edit_label_invalid_post_shows_errors(self):
        # Create a label to edit
        label = Label.objects.create(bar_code='123', description='Old')
        # Post missing required fields to ensure validation errors are surfaced
        response = self.client.post(reverse('labels:edit_label', args=[label.id]), {
            # intentionally omit required fields like description and label_types
            'bar_code': '123',
        })
        self.assertEqual(response.status_code, 200)
        # Expect at least description to be required
        self.assertIn('description', response.context['form'].errors)
