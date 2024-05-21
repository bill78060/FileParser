import chardet
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from .models import UploadedFile

def homepage(request):
    files = UploadedFile.objects.all()
    return render(request, 'fileLoader/homepage.html', {'files': files})

def upload_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return render(request, 'fileLoader/upload.html', {'error': 'No file selected'})

        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(name)

        raw_data = uploaded_file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()

        uploaded_file_instance = UploadedFile(name=uploaded_file.name, content=content)
        uploaded_file_instance.save()
        return redirect('homepage')

    return render(request, 'fileLoader/upload.html')

def view_file(request, file_id):
    file = get_object_or_404(UploadedFile, pk=file_id)
    return render(request, 'fileLoader/view_file.html', {'file': file})

def edit_file(request, file_id):
    file = get_object_or_404(UploadedFile, pk=file_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        file.content = content
        file.save()
        return redirect('view_file', file_id=file.id)

    return render(request, 'fileLoader/edit_file.html', {'file': file})

def delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, pk=file_id)
    file.delete()
    return redirect('homepage')



# import chardet
# from django.shortcuts import render, redirect, get_object_or_404
# from django.core.files.storage import FileSystemStorage
# from .models import UploadedFile
# from .forms import UploadFileForm
# import re

# def homepage(request):
#     files = UploadedFile.objects.all()
#     return render(request, 'fileLoader/homepage.html', {'files': files})

# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             for uploaded_file in request.FILES.getlist('file'):
#                 fs = FileSystemStorage()
#                 name = fs.save(uploaded_file.name, uploaded_file)
#                 file_path = fs.path(name)

#                 # Detect the encoding of the file
#                 raw_data = uploaded_file.read()
#                 result = chardet.detect(raw_data)
#                 encoding = result['encoding']

#                 # Ensure the file is read with the correct encoding
#                 try:
#                     with open(file_path, 'r', encoding=encoding) as file:
#                         content = file.read()
#                 except Exception as e:
#                     # Handle encoding errors
#                     print(f"Error reading file: {e}")
#                     content = "Error reading file content."

#                 uploaded_file_instance = UploadedFile(name=uploaded_file.name, content=content)
#                 uploaded_file_instance.save()
#             return redirect('homepage')
#     else:
#         form = UploadFileForm()
#     return render(request, 'fileLoader/upload.html', {'form': form})

# def view_file(request, file_id):
#     file = get_object_or_404(UploadedFile, pk=file_id)
#     formatted_content = format_file_content(file.content)
#     return render(request, 'fileLoader/view_file.html', {'file': file, 'formatted_content': formatted_content})

# def edit_file(request, file_id):
#     file = get_object_or_404(UploadedFile, pk=file_id)
#     if request.method == 'POST':
#         content = request.POST.get('content')
#         file.content = content
#         file.save()
#         return redirect('view_file', file_id=file.id)
#     return render(request, 'fileLoader/edit_file.html', {'file': file})

# def delete_file(request, file_id):
#     file = get_object_or_404(UploadedFile, pk=file_id)
#     file.delete()
#     return redirect('homepage')

# def format_file_content(content):
#     # Simple heuristic to detect code snippets and paragraphs
#     lines = content.split('\n')
#     formatted_lines = []

#     for line in lines:
#         if re.match(r'^\s*$', line):  # Empty line
#             formatted_lines.append('<br>')
#         elif re.match(r'^\s*#.*', line):  # Python comments
#             formatted_lines.append(f'<span style="color: #6ac4ff;">{line}</span>')
#         elif re.match(r'^\s*(def|class|import|from|if|else|elif|for|while|try|except|with|return).*', line):  # Python code
#             formatted_lines.append(f'<code>{line}</code>')
#         else:  # Normal paragraph
#             formatted_lines.append(f'<p>{line}</p>')

#     return '\n'.join(formatted_lines)
