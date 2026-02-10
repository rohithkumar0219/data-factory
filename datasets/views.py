from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from .models import Dataset
from .processing import process_file
from django.views.decorators.http import require_POST
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


@login_required
def dashboard(request):
    datasets = Dataset.objects.filter(owner=request.user)
    return render(request, 'dashboard.html', {'datasets': datasets})


@login_required
def upload(request):
    if request.method == 'POST':
        file = request.FILES.get('file')

        if not file:
            return render(request, 'upload.html', {'error': 'No file selected'})

        dataset = Dataset.objects.create(
            owner=request.user,
            raw_file=file,
            name=file.name
        )

        from .processing import process_file
        process_file(dataset)

        return redirect('/dashboard/')

    return render(request, 'upload.html')


@login_required
def download(request, id):
    dataset = Dataset.objects.get(id=id, owner=request.user)

    if not dataset.processed_file:
        return redirect('/dashboard/')

    return FileResponse(
        dataset.processed_file.open(),
        as_attachment=True,
        filename=dataset.processed_file.name
    )
