from datetime import timedelta
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from post.models import Posting, Comment


def new(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        posting = Posting.objects.create(title = title, content = content)
        posting.updated_at = False
        posting.save()
        return redirect('post:detail', posting.id)
    else :
        return render(request, 'post/new.html')

def list(request):
    postings = Posting.objects.all()
    # ts = Posting.objects.filter(title__in=postings)
    q = request.GET.get('q', '')
    print(q)
    if q:
        postings = postings.filter(title__icontains=q)

    return render(request, 'post/list.html', {'postings':postings, 'q':q})

def detail(request, id):
    posting = get_object_or_404(Posting, id=id)
    if posting.updated_at - posting.created_at >= timedelta(seconds=1):
        updated = True
    else :
        updated = False
    comments = Comment.objects.filter(posting=posting).order_by('-id')
    if request.method == 'POST':
        content = request.POST.get('comment_content','')
        comment = Comment.objects.create(posting=posting, content=content)
        return redirect('post:detail', posting.id)
    else:
        return render(request, 'post/detail.html', {'posting':posting, 'comments':comments, 'updated':updated})

def edit(request, id):
    posting = get_object_or_404(Posting, id=id)
    if request.method == 'POST':
        posting.title = request.POST.get('title', '')
        posting.content = request.POST.get('content', '')
        posting.save()
        return redirect('post:detail', id)
    else :
        return render(request, 'post/edit.html', {'posting':posting})

def delete(request, id):
    posting = get_object_or_404(Posting, id=id)
    posting.delete()
    return redirect('post:list')

def comment_delete(request, id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('post:detail', id)