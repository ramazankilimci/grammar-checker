from django.shortcuts import render
from .forms import UserRegistrationForm
from django.contrib.auth.models import User

# Create your views here.

def register(request):
    user_form = UserRegistrationForm(request.POST)
    if request.method == 'POST' and user_form.is_valid:
        try:
            print(request.POST)
            # Create user object but do not commit
            new_user = user_form.save(commit=False)
            
            print('Username:', User.objects.filter(username=user_form.cleaned_data['username']))
            if User.objects.filter(username=user_form.cleaned_data['username']).count() == 0:
                
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
                error_text = 'User name exists.'
                return render(request,
                        'account/register_error.html',
                        {'error_text': error_text})
        except ValueError as e:
            print(e)
            error_text = 'Passwords did not match or username exists.'
            return render(request,
                        'account/register_error.html',
                        {'error_text': error_text})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})
