from django.urls import path , include
from  .import views
from .views import get_client_real_ip
from .views import upload_image


urlpatterns = [
    path('recognize/', views.recognize_face, name='recognize_face'),
    path('api/', include('api.urls'))
]

urlpatterns = [
    path('get-ip/', get_client_real_ip, name='get-ip'),
]



urlpatterns = [
    path('upload-image/', upload_image, name='upload-image'),
]


urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
]
