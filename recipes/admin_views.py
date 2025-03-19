from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'admin/feedback_list.html', {'feedbacks': feedbacks})
