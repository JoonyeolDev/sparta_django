from django.shortcuts import render, redirect
from .models import TweetModel, TweetComment
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')


def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'tweet': all_tweet})
        else:
            return redirect('/sign-in')
    if request.method == 'POST':
        user = request.user
        my_tweet = TweetModel()
        my_tweet.author = user
        my_tweet.content = request.POST.get('my-content', '')
        my_tweet.save()
        return redirect('/tweet')


@login_required
def detail_tweet(request, id):
    if request.method == 'GET':
        select_tweet = TweetModel.objects.get(id=id)
        all_comment = TweetComment.objects.all()
        return render(request, 'tweet/tweet_detail.html', {'tweet': select_tweet, 'comment': all_comment})


@login_required
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')


@login_required
def write_comment(request, id):
    if request.method == 'POST':
        comment = request.POST.get("comment", "")
        current_tweet = TweetModel.objects.get(id=id)

        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()

        return redirect('/tweet/' + str(id))


def delete_comment(request, id):
    my_comment = TweetComment.objects.get(id=id)
    my_comment.delete()
    return redirect('/tweet/' + str(my_comment.tweet_id))
