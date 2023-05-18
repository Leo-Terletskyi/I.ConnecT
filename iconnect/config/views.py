from django.shortcuts import redirect


def redirect_to_user_acc(request):
    if request.user.is_authenticated:
        return redirect('user_acc', pk=request.user.id)
    return redirect('sign_in')
