# views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NoteSerializer
from .models import Note
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.conf import settings

class NoteListAPIView(APIView):
    """List all notes or create new note"""

    def get(self, request):
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Note added successfully!',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDetailAPIView(APIView):
    """Get, update or delete a note"""

    def get_object(self, pk):
        try:
            return Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            return None

    def get(self, request, pk):
        note = self.get_object(pk)
        if not note:
            return Response(
                {'error': 'Note not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def put(self, request, pk):
        note = self.get_object(pk)
        if not note:
            return Response(
                {'error': 'Note not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Note updated successfully!',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        note = self.get_object(pk)
        if not note:
            return Response(
                {'error': 'Note not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        note.delete()
        return Response(
            {'message': 'Note deleted successfully!'},
            status=status.HTTP_204_NO_CONTENT
        )
# views.py XSS-Vulnerable      
def xss_vulnerable(request):
    output = ""
    if request.method == "POST":
        user_input = request.POST.get("content", "")
        output = mark_safe(user_input)
    return render(request, 'notes/xss_demo.html', {'output': output, 'safe': False})

# views.py XSS - Secure
def xss_secure(request):
    output = ""
    if request.method == "POST":
        user_input = request.POST.get("content", "")
        output = user_input  # no mark_safe here
    return render(request, 'notes/xss_demo.html', {'output': output, 'safe': True})

# views.py SQL Injection - Vulnerable
def sqli_vulnerable(request):
    results = []
    query_used = ""
    if request.method == "POST":
        search = request.POST.get("search", "")
        query_used = f"SELECT * FROM notes_note WHERE title = '{search}'"
        with connection.cursor() as cursor:
            cursor.execute(query_used)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return render(request, 'notes/sqli_demo.html', {'results': results, 'query': query_used, 'safe': False})

# views.py SQL Injection - Secure
def sqli_secure(request):
    results = []
    if request.method == "POST":
        search = request.POST.get("search", "")
        results = Note.objects.filter(title=search)
    return render(request, 'notes/sqli_demo.html', {'results': results, 'query': "ORM parameterized query", 'safe': True})

@csrf_exempt
def csrf_vulnerable(request):
    message = ""
    if request.method == "POST":
        title = request.POST.get("title", "")
        Note.objects.create(title=title, description="Added via CSRF")
        message = f"Note '{title}' created! (CSRF succeeded)"
    return render(request, 'notes/csrf_demo.html', {'message': message, 'safe': False})

# CSRF - Secure
def csrf_secure(request):
    message = ""
    if request.method == "POST":
        title = request.POST.get("title", "")
        Note.objects.create(title=title, description="Legitimate note")
        message = f"Note '{title}' created securely."
    return render(request, 'notes/csrf_demo.html', {'message': message, 'safe': True})

def env_demo(request):
    context = {
        'secret_key': settings.SECRET_KEY[:20] + '...',  
        'debug': settings.DEBUG,
        'allowed_hosts': settings.ALLOWED_HOSTS,
    }
    return render(request, 'notes/env_demo.html', context)