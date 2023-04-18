from django.shortcuts import render, redirect
from .models import TweetModel, TweetComment
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView

### 중간 생략 #############

class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context

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
        content = request.POST.get('my-content','')
        tags = request.POST.get('tag','').split(',')

        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request,'tweet/home.html',{'error':'글은 공백일 수 없습니다', 'tweet': all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            for tag in tags:
                tag = tag.strip()
                if tag != '':
                    my_tweet.tags.add(tag)

            my_tweet.save()

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
