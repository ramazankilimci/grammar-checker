from django.shortcuts import render
from .forms import SpellCheckForm
from django.http import HttpResponseBadRequest
from . import services
from .models import Spell
from django.contrib.auth.models import AnonymousUser

# Create your views here.
def index(request):
    print("REQUEST: ", request)
    spelled = False
    orig_text = ''
    spelled_text = ''
    if request.method == 'POST':
        form = SpellCheckForm(request.POST)
        print("FORM: ", form)
        if form.is_valid():
            cd = form.cleaned_data
            print("CD: ", cd['spell_text'])
            
            srv = services
            orig_text = cd['spell_text']
            spelled_text = srv.spell_sentence(orig_text)
            spelled = True
            print(request.user.is_anonymous)
            print(AnonymousUser.is_anonymous)
            if not request.user.is_anonymous:
                spell_obj = Spell(orig_text=orig_text, spelled_text=spelled_text, user=request.user)
                spell_obj.save()
    else:
        form = SpellCheckForm()
    print("SPELLED: ", spelled)

    return render(request, 'grammar/index.html', {'orig_text': orig_text, 'spelled_text': spelled_text, 'spelled': spelled})

# Custom AJAX required decorator
def ajax_required(f):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....
    """

    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
