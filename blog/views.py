from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from blog.models import BlogPost
from .serializers import BlogPostSerializer, BlogPostRegister
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse


# Create your views here.
@api_view(['GET'])
def get_route(request):
    return Response([
        'api/register',
        'api/login',
        'api/logout',
        'api/blog',
        'api/blog/<int:id>',
        'api/details',
    ])

@api_view(['POST'])
def register(request):
    serializer = BlogPostRegister(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "user Registered successfully"}, status=201)
    return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user= authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"message": "Login successful"}, status=201)
    else:
        return JsonResponse({"message": "Check your userID or password"}, status=400)

@api_view(['POST'])
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"message":"Logout successed"}, status=200)
    return JsonResponse({"message": "Logout not work"})

@api_view(['POST'])
def blog(request): 
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image') 
     
        try:
            author = User.objects.get(id=1)  
        except User.DoesNotExist:
            return JsonResponse({'error': 'Author user not found'}, status=400)

        blog = BlogPost.objects.create(
            title=title,
            content=content,
            image=image,
            author=author,
        )
        return JsonResponse({'message': 'Blog created successfully', 'id': blog.id}, status=201)
    
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@api_view(['GET'])
def details(request):
    uploads = BlogPost.objects.all().order_by('-upload_at')
    serializer = BlogPostSerializer(uploads, many=True, context={'request': request})
    return Response(serializer.data)