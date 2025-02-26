import json
from django.http import JsonResponse
import face_recognition
from django.contrib.auth.models import User  # Import User model (assuming you're using Django's default User model)
from .api_service import fetch_data


from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from rest_framework.response import Response

def get_external_data(request):
    data = fetch_data()
    return JsonResponse(data, safe=False)

def get_client_real_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # إذا كان السيرفر خلف Proxy
    else:
        ip = request.META.get('REMOTE_ADDR')  # الحصول على IP الحقيقي

    return JsonResponse({"ip": ip})



def recognize_face(request):
    if request.method == "POST":
        if 'image' not in request.FILES:
            return JsonResponse({"status": "failure", "message": "No image provided."})

        image = request.FILES['image']
        try:
            # Load the image file
            img = face_recognition.load_image_file(image)

            # Get face encodings
            face_encodings = face_recognition.face_encodings(img)
            
            if face_encodings:
                encoding = face_encodings[0]  # Assuming the first face in the image

                # Retrieve all users from the database
                users = User.objects.all()
                
                for user in users:
                    # Assume the encoding is stored as a JSON string in user.face_encoding
                    try:
                        stored_encoding = json.loads(user.profile.face_encoding)  # Assuming `face_encoding` is stored in the `profile`
                    except (json.JSONDecodeError, AttributeError):
                        continue  # Skip users with no valid encoding

                    match = face_recognition.compare_faces([stored_encoding], encoding)

                    if match[0]:  # If a match is found
                        return JsonResponse({"status": "success", "name": user.username})

                return JsonResponse({"status": "failure", "message": "Face not recognized."})

            return JsonResponse({"status": "failure", "message": "No faces found in the image."})
        
        except Exception as e:
            # Handle unexpected errors
            return JsonResponse({"status": "failure", "message": f"Error processing image: {str(e)}"})

    return JsonResponse({"status": "failure", "message": "Invalid request method. Use POST."})




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

# مجلد لحفظ الصور
UPLOAD_DIR = "uploaded_images/"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@csrf_exempt  # تعطيل CSRF لحين التجربة
def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        image_path = os.path.join(UPLOAD_DIR, image.name)

        with open(image_path, "wb+") as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        return JsonResponse({"status": "success", "message": "تم حفظ الصورة", "image_path": image_path})
    else:
        return JsonResponse({"status": "error", "message": "لم يتم استلام الصورة"}, status=400)




@csrf_exempt
@api_view(['POST'])
def upload_image(request):
    name = request.data.get('name')
    id = request.data.get('id')
    image = request.FILES.get('image')

    if name and id and image:
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        file_url = fs.url(filename)
        
        return Response({'status': 'success', 'file_url': file_url})
    else:
        return Response({'status': 'failed', 'message': 'Missing fields'}, status=400)
