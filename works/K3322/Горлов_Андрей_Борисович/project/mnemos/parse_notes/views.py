from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import ContactForm, UploadFileForm
import os
from django.shortcuts import render
from parse_notes.pipeline.process_notes import full_pipeline
from django.conf import settings


def home(request):
    return render(request, 'parse_note/home.html')


def about(request):
    return render(request, 'parse_note/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = ContactForm()
    return render(request, 'parse_note/contact.html', {'form': form})


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_url = fs.url(filename)
            return render(request, 'parse_note/upload_success.html', {'file_url': file_url})
    else:
        form = UploadFileForm()
    return render(request, 'parse_note/upload.html', {'form': form})


def start_processing(request):
    # Просто отдаем HTML "Идет обработка..."
    return render(request, 'parse_note/process.html')


def process_all_notes(request):
    # Запускаем обработку файлов
    media_dir = settings.MEDIA_ROOT
    full_pipeline(media_dir)
    return redirect('process_success')


def process_success(request):
    # Страница успешной обработки
    media_dir = settings.MEDIA_ROOT
    files = [f for f in os.listdir(media_dir) if os.path.isfile(os.path.join(media_dir, f))]
    return render(request, 'parse_note/process_success.html', {'files': files})
