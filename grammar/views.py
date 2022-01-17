from django.shortcuts import render
from .forms import SpellCheckForm
from django.http import HttpResponseBadRequest
from . import services
from .models import Mistake, Spell
from django.contrib.auth.models import AnonymousUser
import datetime
from django.contrib.auth.models import User
import json
from actions.utils import create_action, delete_action
from actions.models import Action
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


home_url = 'http://justgram.com'

# Create your views here.
def index(request):
    """
    Returns the homepage of the application.
    If spell text is provided by the user,
    it returns the spelled text.
    """
    print("REQUEST: ", request)
    spelled = False
    orig_text = ''
    spelled_text_html = ''
    if request.method == 'POST':
        form = SpellCheckForm(request.POST)
        print("FORM: ", form)
        if form.is_valid():
            cd = form.cleaned_data
            print("CD: ", cd['spell_text'])
            
            srv = services
            orig_text = cd['spell_text']
            # orig_text_list = orig_text.split('.')
            # spelled_list = []
            # for text in orig_text_list:
            #     temp_spelled_list = srv.spell_sentence_with_mark(text)
            #     spelled_list +=temp_spelled_list
            #     print("Spelled List:", spelled_list) 
            spelled_list = srv.spell_sentence_with_mark(orig_text)
            new_list = []
            #if not request.user.is_anonymous:
            for spell in spelled_list:
                    if spell[1] == 1:
                        if not request.user.is_anonymous:
                            mistake = Mistake(user=request.user, wrong_word=spell[2], right_word=spell[0])
                            mistake.save() # Creates a record in database
                        spell[0] = "<span class=\"bg-warning text-dark\">" + spell[0] + "</span>"
                        print(spell[0])
                    new_list.append(spell[0])
            spelled_text_html = ' '.join(new_list)

            # Used to show user the corrected words
            spelled_text_html = mark_safe(spelled_text_html)

            # Used to save spelled text into database
            spelled_text = srv.spell_sentence(orig_text)


            print("Spelled text:", spelled_text)
            spelled = True
            print(request.user.is_anonymous)
            print(AnonymousUser.is_anonymous)

            # Inside the IF condition, JSON-LD is created for Activity Stream
            # Also it saves the original and spelled text into Spell modl
            if not request.user.is_anonymous:
                spell_obj = Spell(orig_text=orig_text, spelled_text=spelled_text, user=request.user)
                spell_obj.save()
                
                published_date = get_published_date()
                actor_profile_url = get_user_profile_url(request.user.id)
                actor_fullname = get_user_fullname(request.user)

                target_spell_url = get_spell_text_url(spell_obj.id)
                object_spell_url = get_spell_text_url(spell_obj.id)

                w3c_json = json.dumps({
                            "@context": "https://www.w3.org/ns/activitystreams",
                            "summary": "{} spelled {} to {}".format(actor_fullname, orig_text, spelled_text),
                            "type": "Create",
                            "published": published_date,
                            "actor": {
                                "type": "Person",
                                "id": actor_profile_url,
                                "name": actor_fullname,
                                "url": actor_profile_url
                            },
                            "object": {
                                "id": target_spell_url,
                                "type": "Note",
                                "url": target_spell_url,
                                "name": orig_text,
                            },
                            "target": {
                                "id": object_spell_url,
                                "type": "Note",
                                "url": object_spell_url,
                                "name": spelled_text,
                            }
                        })
                print(w3c_json)

                # Action is saved into ACTION model in ACTIONS app
                # This is completely separate model from the main application
                create_action(request.user, verb=1, activity_json=w3c_json, target=spell_obj)
            else:
                form = SpellCheckForm()

    return render(request, 'grammar/index.html', {'orig_text': orig_text, 'spelled_text_html': spelled_text_html, 'spelled': spelled})

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

def get_published_date():
    """
    Returns the published date for activity in ISO format.
    """
    return str(datetime.datetime.now().isoformat())

# Gets user id as input and returns user profile
def get_user_profile_url(user_id):
    """
    Returns the user profile url for activity stream.
    """
    return home_url + "/user/" + str(user_id)


# Gets user object as input and returns User's Full Name
def get_user_fullname(user):
    """
    Returns the user full name for activity stream.
    """
    return str(user.first_name + " " + user.last_name)

def get_spell_text_url(spell_id):
    """
    Returns the spell text url for activity stream.
    """
    return home_url + '/spell/' + str(spell_id)

def spellings(request):
    """
    Returns the SPELLINGS of the user.
    Gets activity from ACTION model in ACTIONS app.
    """
    # print("User Last Login:", request.user.last_login)
    # actor_user_last_login = request.user.last_login.replace(tzinfo=None)
    activities = []
    if not request.user.is_anonymous:
        user_actions = Action.objects.filter(user_id=request.user.id)
        for action in user_actions:
            print(action.action_json)
        #deserialized = serializers.deserialize('json', user.action_json)
            print(json.loads(action.action_json)['published'])
            last_action = json.loads(action.action_json)
            published_date = last_action['published']
            activity_published_date = datetime.datetime.strptime(published_date[:-7], '%Y-%m-%dT%H:%M:%S')
            # if activity_published_date > actor_user_last_login:
            action_type = last_action['type']
            action_actor_name= last_action['actor']['name']
            action_actor_url = last_action['actor']['url']
            action_object_name = last_action['object']['name']
            action_object_url = last_action['object']['url']
            action_target_name = last_action['target']['name']
            action_target_url = last_action['target']['url']
            actionId = action.id
            activities.append([ action_type,
                                action_actor_name,
                                action_actor_url,
                                action_object_name,
                                action_object_url,
                                action_target_name,
                                action_target_url,
                                activity_published_date,
                                actionId
                                ])
            print("Date is ", True)
    return render(request, 'grammar/spellings.html', {'activities': activities})

def most_made_mistakes(request):
    """
    Returns the most common mistakes for the user.
    Relate information is gotten from MISTAKES model in GRAMMAR app.
    """
    mistakes = []
    if not request.user.is_anonymous:
        mistakes = Mistake.objects.filter(user=request.user).values('wrong_word', 'right_word', 'user').annotate(total=Count('wrong_word')).order_by('-total')
    return render(request, 'grammar/mistakes.html', {'mistakes': mistakes})

def profile(request):
    return render(request, 'grammar/profile.html')

@csrf_exempt
@ajax_required
@require_POST
@login_required
def spelling_delete(request):
    """
    Deletes the specific spelling for the user.
    Items are deleted from the ACTION model in the ACTIONS app.
    """
    print("Spelling delete id:", request.POST.get('id'))
    try:
        action_id = request.POST.get('id')
        action_obj = Action.objects.get(pk=action_id)
        action_obj.delete()
        return JsonResponse({'status': 'ok'})
    except:
        return JsonResponse({'status': 'error'})

def language(request):
    """
    Returns the supported languages.
    """
    languages = ['Turkish', 'English', 'Spanish']
   
    return render(request, 'grammar/language.html', {'languages': languages})

def apiusage(request):
    return render(request, 'grammar/apiusage.html')