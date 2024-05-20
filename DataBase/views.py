from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from Accounts.models import * 
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.core.files.base import ContentFile
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from datetime import datetime


@login_required
# Create your views here.
def dashboard(request):
    user = request.user 
    movies = Movies.objects.filter(user = user).count()
    music = Music.objects.filter(user = user).count()
    videos = Videos.objects.filter(user = user).count()
    photos = Photos.objects.filter(user = user).count()
    data = UserSession.objects.all().values()
    
    file = movies + music + videos + photos
    context = {
        'movies': movies,
        'music': music,
        'videos': videos,
        'photos': photos,
        'file':file,        
    }
    return render(request, 'dashboard.html',context)



@login_required
def music(request):
    mymusic = Music.objects.filter(user=request.user)
    context = {'music': mymusic}
    return render (request, 'music.html', context)


@login_required
def movies(request):
        mymovies = Movies.objects.filter(user=request.user)
        context = {'movies': mymovies}
        return render (request, 'movies.html',context)
        

@login_required
def videos(request):
    myvideo = Videos.objects.filter(user=request.user)
    context = {'videos': myvideo}
    return render (request, 'videos.html',context)

@login_required
def photos(request):
    myphotos = Photos.objects.filter(user=request.user)
    context = {'photos': myphotos}            
    return render (request, 'photos.html',context)


@login_required
def files(request):

    user = request.user 
    movies = Movies.objects.filter(user = user).count()
    music = Music.objects.filter(user = user).count()
    videos = Videos.objects.filter(user = user).count()
    photos = Photos.objects.filter(user = user).count()
    
    context = {
        'movies': movies,
        'music': music,
        'videos': videos,
        'photos': photos,
    }
    return render (request, 'files.html',context)
def profile(request):
    return render (request, 'profile.html')

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


@login_required

def profile_update(request,val):
    if request.method == 'POST':
        image = request.FILES.get('image')
        val = val
        current_username = request.user.username
        
        if request.user.is_authenticated:
            user = MyUser.objects.filter(username=current_username).first()
           
            
            if user:
                user.image.delete()
                img = Image.open(image)
                
                # Convert image to RGB if it has an alpha channel
                if img.mode in ("RGBA", "LA"):
                    img = img.convert("RGB")
                
                # Get the dimensions of the image
                width, height = img.size
                
                # Crop the image to a square (1:1 aspect ratio)
                min_dim = min(width, height)
                left = (width - min_dim) / 2
                top = (height - min_dim) / 2
                right = (width + min_dim) / 2
                bottom = (height + min_dim) / 2
                img = img.crop((left, top, right, bottom))
                
                # Save the cropped image to an in-memory file
                img_io = BytesIO()
                img.save(img_io, format='JPEG')
                img_io.seek(0)
                
                # Create a Django file object from the in-memory file
                cropped_image = InMemoryUploadedFile(
                    img_io, None, 'profile.jpg', 'image/jpeg', sys.getsizeof(img_io), None
                )
                
                # Save the file to the user's image field
                user.image.save('profile.jpg', cropped_image)
                
                # Save the user object
                user.save()
                if val == 1:
                    return redirect(reverse('settings'))
                else :
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
     
    # return redirect(reverse('settings'))
@login_required
def settings(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dob = request.POST['dob']
        email = request.POST['email']
        bio = request.POST['bio']
        
        # Get the current user's username
        current_username = request.user.username
        
        if request.user.is_authenticated:
            # Filter MyUser instances based on the username
            
                user = request.user 
                # Update the user profile fields
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.dob = dob
                user.bio = bio
                
                # Save the changes
                user.save()
                
                return redirect(reverse('settings'))
        
    return render(request, 'settings.html')




@login_required
def music_edit(request):
    mymusic = Music.objects.filter(user=request.user)
    context = {'music': mymusic}

    if request.method == 'POST' and request.FILES.getlist('file'):
        for file in request.FILES.getlist('file'):
            title = file.name
            music = Music.objects.create(title=title, file=file, user=request.user)
            
            try:
                # Open the MP3 file
                audio = MP3(file, ID3=ID3)

                # Check if the audio file has ID3 tags
                if audio.tags:
                    # Get the album art
                    for tag in audio.tags.values():
                        if isinstance(tag, APIC):
                            image_data = tag.data
                            # Save the image data to the image field
                            music.image.save(f'{title}.jpg', ContentFile(image_data), save=True)
                            break
            except Exception as e:
                print(f"An error occurred while extracting album art: {e}")

            

    return render(request, 'music_edit.html', context)


@login_required
def movies_edit(request):
        mymovies = Movies.objects.filter(user=request.user)
        context = {'movies': mymovies}

        if request.method == 'POST' :
             file = request.FILES.get('file')
             title = request.POST['title']
             
             movie = Movies.objects.create(title=title,  file=file, user=request.user)
             movie.save()
            
       
        return render (request, 'movies_edit.html',context)
        

@login_required
def videos_edit(request):
    myvideo = Videos.objects.filter(user=request.user)
    context = {'videos': myvideo}
    if request.method == 'POST' and request.FILES.getlist('file'):
        for file in request.FILES.getlist('file'):
            title = file.name
            videos = Videos.objects.create(title=title,  file=file, user=request.user)
            videos.save()
    return render (request, 'videos_edit.html',context)




@login_required
def photos_edit(request):
    myphotos = Photos.objects.filter(user=request.user)
    context = {'photos': myphotos}

    
    if request.method == 'POST' and request.FILES.getlist('file'):
        for file in request.FILES.getlist('file'):
            title = file.name
            photo = Photos.objects.create(title=title,  file=file, user=request.user)
            photo.save()
        
        
    return render (request, 'photos_edit.html',context)

@login_required

def delete_record(request,val,pk):
    user_id =0
    photo = 1
    music = 2
    movie = 3
    video = 4
    img = 5
    if val == photo:
            obj = get_object_or_404(Photos, pk=pk)
            obj.delete()
            return redirect(reverse('photos_edit'))
    elif val == music:
        obj = get_object_or_404(Music, pk=pk)
        obj.delete()
        return redirect(reverse('music_edit'))
    elif val == movie:
        obj = get_object_or_404(Movies, pk=pk)
        obj.delete()
        return redirect(reverse('movies_edit'))
    elif val == video:
        obj = get_object_or_404(Videos, pk=pk)
        obj.delete()
        return redirect(reverse('videos_edit'))
    elif val == user_id:
        user = request.user.username
        try:
            custom_user = MyUser.objects.get(username=user)
            custom_user.delete()  # This will delete the user and trigger any cascading deletes
            return redirect(reverse('index'))
        except MyUser.DoesNotExist:
            pass 
            return redirect(reverse('index'))
        
    elif val == img:
       user = request.user
       if user.image:
        user.image.delete()  # This deletes the image file from storage
        user.image = None    # This clears the image field in the database
        user.save()          # Save the user instance to apply the changes
        messages.success(request, "Your image has been deleted successfully.")
        return redirect(reverse('settings'))
       else:
            messages.error(request, "You do not have an image to delete.")
            return redirect('profile')


def change_password_logged(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Check if the current password matches the user's actual password
        if not check_password(current_password, user.password):
            messages.error(request, 'Incorrect current password.')
            return redirect('change_password_logged')

        # Check if the new password and confirm password match
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect(reverse('change_password_logged'))

        # Update the user's password
        user.set_password(new_password)
        user.save()

        # Update session with new user credentials
        update_session_auth_hash(request, user)

        messages.success(request, 'Your password was successfully updated!')
        return redirect(reverse('settings'))  # Redirect to success page

    return render(request, 'change_password_logged.html')