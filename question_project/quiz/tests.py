from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Question, QuestionHistory

class CSVUploadAtomicityTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_atomicity_on_csv_upload_failure(self):
        # Create a fake CSV with one good row and one bad row (missing correct_answer)
        csv_data = (
            "text,option_a,option_b,option_c,option_d,correct_answer\n"
            "What is 2+2?,2,3,4,5,A\n"
            "Incomplete question,10,20,30,40,\n"  # Missing correct_answer
        ).encode('utf-8')

        uploaded_file = SimpleUploadedFile("questions.csv", csv_data, content_type="text/csv")

        response = self.client.post('/upload/', {'csv_file': uploaded_file})

        # Expect the upload to fail and nothing to be saved
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(QuestionHistory.objects.count(), 0)

        # Optionally, check if error was rendered
        self.assertContains(response, "error", status_code=200)
