from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from .models import Dataset
from .processing import process_csv


@login_required
def dashboard(request):
    datasets = Dataset.objects.filter(owner=request.user)
    return render(request, 'dashboard.html', {'datasets': datasets})


@login_required
def upload(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file or not file.name.endswith('.csv'):
            return render(request, 'upload.html', {'error': 'Only CSV files allowed'})

        dataset = Dataset.objects.create(
            owner=request.user,
            raw_file=file,
            name=file.name
        )
        process_csv(dataset)
        return redirect('/dashboard/')

    return render(request, 'upload.html')


@login_required
def download(request, id):
    dataset = Dataset.objects.get(id=id, owner=request.user)
    return FileResponse(dataset.processed_file.open(), as_attachment=True)
