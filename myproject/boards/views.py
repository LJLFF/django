from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Board, Topic, Post
from django.contrib.auth.decorators import login_required
from .forms import NewTopicForm
from django.http import Http404
# Create your views here.
def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})
def board_topics(request, pk):
    # try:
    #     board = Board.objects.get(pk=pk)
    # except Board.DoesNotExist:
    #     raise Http404
    # return render(request, 'topics.html', {'board': board})
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})

from django.contrib.auth.decorators import login_required
@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
            message=form.cleaned_data.get('message'),
            topic=topic,
            created_by=request.user)
            return redirect('board_topics', pk=board.pk) # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic})