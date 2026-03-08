from django.test import TestCase
from django.urls import reverse
from .models import Note

class NoteModelTest(TestCase):

    def test_notes_can_be_created(self):
        note = Note.objects.create(
            title="Test Note",
            description="This is a valid description"
        )
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(note.description, "This is a valid description")

    def test_error_occurs_if_description_is_less_than_10_chars_long(self):
        response = self.client.post(reverse('notes:note-list'), {
            'title': 'Test Note',
            'description': 'short'  # less than 10 chars
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('description', response.data)