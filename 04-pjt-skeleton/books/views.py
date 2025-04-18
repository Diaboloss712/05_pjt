from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Thread
from accounts .models import User
from .forms import ThreadForm, BookForm
from .utils import (
    process_wikipedia_info,
    generate_author_gpt_info,
    generate_audio_script,
    create_tts_audio,
)


def index(request):
    books = Book.objects.all()
    context = {
        "books": books,
    }
    return render(request, "books/index.html", context)

@login_required
def create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)

            wiki_summary = process_wikipedia_info(book)

            author_info, author_works = generate_author_gpt_info(
                book, wiki_summary
            )
            book.author_info = author_info
            book.author_works = author_works
            book.user = request.user
            book.save()

            audio_script = generate_audio_script(book, wiki_summary)

            audio_file_path = create_tts_audio(book, audio_script)
            if audio_file_path:
                book.audio_file = audio_file_path
                book.save()

            return redirect("books:detail", book.pk)
    else:
        form = BookForm()
    context = {"form": form}
    return render(request, "books/create.html", context)

def detail(request, pk):
    book = Book.objects.get(pk=pk)
    context = {
        "book": book,
    }
    return render(request, "books/detail.html", context)

@login_required
def update(request, pk):
    book = Book.objects.get(pk=pk)
    if request.user != book.user_id:
        return redirect('books:detail', pk)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect("books:detail", pk)
    else:
        form = BookForm(instance=book)
    context = {
        "form": form,
        "book": book,
    }
    return render(request, "books/update.html", context)

@login_required
def delete(request, pk):
    book = Book.objects.get(pk=pk)
    book.delete()
    return redirect("books:index")

@login_required
def thread_create(request, pk):
    if request.method == "POST":
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("books:detail", pk)
    else:
        form = ThreadForm()
    context = {"form": form}
    return render(request, "threads/create.html", context)


def thread_detail(request, pk, thread_pk):
    book = Book.objects.get(pk=pk)
    thread = Thread.objects.get(pk=thread_pk)
    context = {
        'thread':thread,
        'book':book,
    }
    return render(request, "threads/detail.html", context)

@login_required
def thread_update(request, pk, thread_pk):
    thread = Thread.objects.get(pk=thread_pk)
    if request.user != thread.user:
        return redirect('book:thread_detail', pk, thread_pk)
    if request.method == "POST":
        form = ThreadForm(request, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("books:detail", pk)
    else:
        form = ThreadForm(request)
    context = {
        "form": form,
        "thread": thread,
    }
    return render(request, "threads/update.html", context)