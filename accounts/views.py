from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Profile
from .forms import RegisterForm, FaceLoginForm
from .face_service import register_face, verify_face
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            profile = Profile.objects.create(user=user)

            if request.FILES.get('face_image'):
                image_bytes = request.FILES['face_image'].read()
                face_id = register_face(image_bytes)
                if face_id:
                    profile.face_id = face_id
                    profile.face_image = request.FILES['face_image']
                    profile.save()

            login(request, user)
            return redirect('/dashboard/')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def face_login(request):
    error = None

    if request.method == 'POST':
        form = FaceLoginForm(request.POST, request.FILES)
        if form.is_valid():
            image_bytes = request.FILES['face_image'].read()
            face_id = verify_face(image_bytes)

            if face_id:
                profile = Profile.objects.filter(face_id=face_id).first()
                if profile:
                    login(request, profile.user)
                    return redirect('/dashboard/')
                else:
                    error = "Face not linked to any user"
            else:
                error = "Face not recognized"
    else:
        form = FaceLoginForm()

    return render(request, 'registration/face_login.html', {
        'form': form,
        'error': error
    })


def logout_view(request):
    logout(request)
    return redirect('/')
