from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Review
from .forms import ReviewForm
# from django.contrib import messages

def reviewhome(request):
    reviews = Review.objects.all()
    reviews_list = Review.objects.all()
    paginator = Paginator(reviews_list, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'r_home.html', {'reviews':reviews, 'posts':posts})

def detail(request, id):
    review = get_object_or_404(Review, pk = id)
    return render(request,'r_detail.html',{'review':review})

def new(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.pub_date = timezone.now()
            new_review.save()
            return redirect('detail', new_review.id)
        else:
            return render(request, 'r_new.html', {'form':form})
    else:
        form = ReviewForm()
        return render(request, 'r_new.html', {'form':form})

def edit(request, id):
    update_review = get_object_or_404(Review, pk = id)
    if request.method == 'POST':
        edit_form = ReviewForm(request.POST, request.FILES, instance = update_review)
        if edit_form.is_valid():
            update_review = edit_form.save(commit = False)
            update_review.pub_date = timezone.now()
            update_review.save()
            #return redirect('/detail/', str(id))
        return redirect('/review/detail/' + str(id))
    else:
        edit_form = ReviewForm(instance = update_review)
        return render(request, 'r_edit.html', {'edit_form':edit_form})

def delete(request, id):
    delete_review = delete_review.objects.get(id = id)
    delete_review.delete()
    return redirect('reviewhome')