from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post,Comment
from .forms import PostForm,CommentForm
from django.urls import reverse_lazy
# import the mixins module which restricts users from posting if not logged in
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,
                                    DetailView,CreateView,
                                    UpdateView,DeleteView)

# Create your views here.

# create a view for the about page
class AboutView(TemplateView):

    template_name = 'Blog/about.html'


# create a list view for the post model
class PostListView(ListView):

    # set the model for the view
    model = Post

    # get_queryset method that decribes how to grab the list based on a queryset
    # (basically SQL query) converted to django built in queryset.
    def get_queryset(self):
        # basically we grab the Post model, all the objects in the model, filter
        # based on the published date. '__lte' is a filter method which says lessthan
        # or equal to. filter based on the current time zone and order by the
        # published date. the '-' describes the acending order of the date
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


# create a detail view to display the contents of the particular post
class PostDetailView(DetailView):

    # set the model
    model = Post


# create a Createview for the post model, inherited from mixins and create view
class PostCreateView(LoginRequiredMixin,CreateView):

    # necesaary attributes to be set, atrribute name cannot be changed
    # url if the user is not logged in, we redirect the user to login page
    login_url = '/login/'
    # after creating a post we redirect the user to the detail view
    redirect_field_name = 'Blog/post_detail.html'
    # set the form class to the post form
    form_class = PostForm
    # set the model
    model = Post

# ccreate a update view if user wants to update the posts
class PostUpdateView(LoginRequiredMixin,UpdateView):

    # necesaary attributes to be set, atrribute name cannot be changed
    # url if the user is not logged in, we redirect the user to login page
    login_url = '/login/'
    # after creating a post we redirect the user to the detail view
    redirect_field_name = 'Blog/post_detail.html'
    # set the form class to the post form
    form_class = PostForm
    # set the model
    model = Post

# create a delete view if the user wants to delete the post
class PostDeleteView(LoginRequiredMixin,DeleteView):

    # set the model
    model = Post
    # success url to redirect the user once the post is deleted
    # make sure that the success_url is activate donly after deleting the post
    # reverse_lazy helps in activating this only when the post is deleted
    success_url = reverse_lazy('post_list')

# create a draft list view in case if there are any drafts that user wants to
# publish retireve only the drafts using get_queryset
class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'Blog/post_list.html'
    model = Post

    # get_queryset method to retrieve only the posts that donot have published_date
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


#############################################################################
#############################################################################
#############################################################################

# create a function to publish the posts
@login_required
def post_publish(request,pk):
    # create a object for post model
    post = get_object_or_404(Post,pk=pk)
    # publish the post
    post.publish()
    # redirect the user to the post detail page
    return redirect('post_detail',pk=pk)

# comments section
# create a function to publish the comments on the posts
@login_required
def add_comment_to_post(request,pk):
    # create a post object with get_object_or_404
    # get_object_or_404 means user didnt find the form
    post = get_object_or_404(Post,pk=pk)

    # check if the user has posted a comment on the post
    if request.method == 'POST':
        # create a form object for commentform
        form = CommentForm(request.POST)

        # check if the form is valid
        if form.is_valid():
            # grab the posted comment and save it to the model
            comment = form.save(commit=False)
            # connect that particular comment for the post to the Post object
            comment.post = post
            comment.save()
            # redirect the user to the post detail page with pk
            return redirect('post_detail',pk=post.pk)

        # if the user has not posted any comment
    else:
        form = CommentForm()
    # render the comment form
    return render(request,'Blog/comment_form.html',{'form':form})

# function to approve the comments for the particular post, login required to
# approve the comments
@login_required
def comment_approve(request,pk):
    # create a comment object with the primary key
    comment = get_object_or_404(Comment,pk=pk)
    # call the method defined in the comment model
    comment.approve()
    # redirect the user to the post_detail page
    return redirect('post_detail',pk=comment.post.pk)

# create a function to remove the comments from the post, login_required to
# remove the comments
@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    # create a varibale to assign the primary key of the post to save the pk,
    # once the comment is deleted we cannot retrieve the pk of that comment
    post_pk = comment.post.pk
    # delete the comment from the database
    comment.delete()
    # redirect the user to the post detail view
    return redirect('post_detail',pk=post_pk)
