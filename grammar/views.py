from django.shortcuts import render
from .forms import SpellCheckForm
from django.http import HttpResponseBadRequest
from . import services
from .models import Spell
from django.contrib.auth.models import AnonymousUser
import datetime
from django.contrib.auth.models import User
import json
from actions.utils import create_action, delete_action
from actions.models import Action

home_url = 'http://justgram.com'

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

                create_action(request.user, verb=1, activity_json=w3c_json, target=spell_obj)
            else:
                form = SpellCheckForm()
    print("SPELLED: ", spelled)

    # Save Spell action
    # Target user object gets using below query
    # user = User.objects.get(id=request.user.id)

    # Save Spell Text



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

def get_published_date():
    return str(datetime.datetime.now().isoformat())


# Gets user id as input and returns user profile
def get_user_profile_url(user_id):
    return home_url + "/user/" + str(user_id)


# Gets user object as input and returns User's Full Name
def get_user_fullname(user):
    return str(user.first_name + " " + user.last_name)

def get_spell_text_url(spell_id):
    return home_url + '/spell/' + str(spell_id)


def spellings(request):
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
            activities.append([ action_type,
                                action_actor_name,
                                action_actor_url,
                                action_object_name,
                                action_object_url,
                                action_target_name,
                                action_target_url
                                ])
            print("Date is ", True)
    return render(request, 'grammar/spellings.html', {'activities': activities})