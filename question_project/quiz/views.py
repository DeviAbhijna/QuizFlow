from django.shortcuts import render, redirect
from .models import Question, QuestionHistory
from django.db import transaction
import csv
from io import TextIOWrapper
from django.utils.timezone import now

def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        try:
            with transaction.atomic():
                reader = csv.DictReader(TextIOWrapper(csv_file.file, encoding='utf-8'))
                for row in reader:
                    q = Question.objects.create(
                        text=row['text'],
                        option_a=row['option_a'],
                        option_b=row['option_b'],
                        option_c=row['option_c'],
                        option_d=row['option_d'],
                        correct_answer=row['correct_answer']
                    )
                    QuestionHistory.objects.create(
                        question_text=q.text,
                        action='ADD',
                        timestamp=now(),
                        details='Imported via CSV'
                    )
            return redirect('show_questions')
        except Exception as e:
            return render(request, 'quiz/upload.html', {'error': str(e)})
    return render(request, 'quiz/upload.html')

def show_questions(request):
    questions = Question.objects.all()
    return render(request, 'quiz/questions.html', {'questions': questions})

def modification_history(request):
    history = QuestionHistory.objects.all().order_by('-timestamp')
    return render(request, 'quiz/mod_history.html', {'history': history})