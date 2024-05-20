from django.urls import path
from .views import *

urlpatterns = [
    path('music/', music , name='music'),
    path('movies/', movies , name='movies'),
    path('videos/', videos , name='videos'),
    path('photos/', photos , name='photos'),
    path('files/', files , name='files'),
    path('profile/', profile , name='profile'),
    path('settings/', settings , name='settings'),
    path('settings/change_password', change_password_logged , name='change_password_logged'),
    path('settings/image/<val>', profile_update , name='profile_update'),
    path('', dashboard , name='dashboard'),
    path('files/music/', music_edit , name='music_edit'),
    path('files/movies/', movies_edit , name='movies_edit'),
    path('files/videos/', videos_edit , name='videos_edit'),
    path('files/photos/', photos_edit , name='photos_edit'),
    path('delete/<int:val>/<int:pk>/', delete_record, name='delete_record'),
    # path('upload/', upload_music, name='upload_music'),
    
]