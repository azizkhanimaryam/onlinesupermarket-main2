from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Comment
from .forms import CommentForm

@login_required
def comment_page(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # Check if the user is authenticated and exists
            if request.user and request.user.is_authenticated:
                comment.user = request.user  # Set the current user
                comment.save()
                messages.success(request, "پیام شما با موفقیت ارسال شد، با تشکر!")  # Success message
            else:
                messages.error(request, "کاربر معتبر نیست. لطفاً دوباره وارد شوید.")  # Error if the user is invalid
            return redirect('comments:comment_page')
    else:
        form = CommentForm()

    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'comment_page.html', {'form': form, 'comments': comments})
