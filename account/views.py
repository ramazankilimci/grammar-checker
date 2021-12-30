from django.shortcuts import render
from .forms import UserRegistrationForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        print(request.POST)
        user_form = UserRegistrationForm(request.POST)
        # Create user object but do not commit
        new_user = user_form.save(commit=False)
        # Set the chosen password
        new_user.set_password(
            user_form.cleaned_data['password']
        )
        print(new_user)
        # Save the user
        new_user.save()

        return render(request,
                      'account/register_done.html',
                      {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})
