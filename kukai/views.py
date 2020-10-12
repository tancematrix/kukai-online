from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Unza, Ku
from django.utils import timezone
import random

class IndexView(generic.ListView):
    model = Unza
    template_name = 'kukai/index.html'
    context_object_name = 'latest_unza_list'
    def get_queryset(self):
        """Return the last five published questions."""
        return Unza.objects.order_by('-pub_date')[:35]


class DetailView(generic.DetailView):
    model = Unza
    template_name = 'kukai/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        context["user"] = user
        if user.is_anonymous:
            unza = context["unza"]
            context['ku_list'] = []
            context['haigo'] = ""
        else:
            unza = context["unza"]
            context['ku_list'] = unza.ku_set.all().filter(author=user)
            context['haigo'] = user.username
        if unza.senku_closed:
            sen_dict = {}
            for selector in unza.selectors.all():
                selected_ku_list = unza.ku_set.all().filter(selectors=selector.id).order_by('author__username')
                sen_dict[selector.username] = selected_ku_list
            context["sen_dict"] = sen_dict
            tenmori_list = []
            for ku in unza.ku_set.all():
                selectors_num = ku.selectors.all().count()
                tenmori_list.append({"ku":ku, "selectors_num":selectors_num, "selectors_num_kansuji":int2kansuji(selectors_num)})
            tenmori_list.sort(key=lambda x:-x["selectors_num"])
            context["tenmori_list"] = tenmori_list
        return context

@login_required
def new(request):
    return render(request, "kukai/new.html")


def create(request):
    try:
        unza_title = request.POST["title"]
        unza_info = request.POST["info"]
    except (KeyError, Unza.DoesNotExist):
        return render(request, 'kukai/new.html', {
            'error_message': "You didn't select a choice.",
        })
    else:
        unza = Unza(pub_date=timezone.now(), author=request.user, unza_title=unza_title, info=unza_info)
        unza.save()
    return HttpResponseRedirect(reverse('kukai:index'))

@login_required
def toku(request, unza_id):
    unza = get_object_or_404(Unza, pk=unza_id)
    return render(request, "kukai/toku.html", {"unza":unza, "user": request.user, "ku":None})


@require_POST
def save_haiku(request, unza_id):
    unza = get_object_or_404(Unza, pk=unza_id)
    try:
        haiku_text = request.POST["haiku_text"]
        ku_id = int(request.POST["ku_id"])
    except (KeyError):
        return render(request, 'kukai/senku.html', {
            'error_message': "投句エラー",
        })
    else:
        if ku_id == -1:
            ku = Ku(author=request.user, unza=unza, haiku_text=haiku_text)
        else:
            ku = get_object_or_404(Ku, pk=ku_id)
            ku.haiku_text = haiku_text
        ku.save()
    return HttpResponseRedirect(reverse('kukai:detail', args=(unza_id,)))


@login_required
def edit_haiku(request, unza_id, ku_id):
    ku = get_object_or_404(Ku, pk=ku_id)
    unza = get_object_or_404(Unza, pk=unza_id)
    return render(request, "kukai/toku.html", {"unza":unza, "user": request.user, "ku":ku})

@require_POST
def delete_haiku(request, unza_id, ku_id):
    ku = get_object_or_404(Ku, pk=ku_id)
    ku.delete()
    return redirect("kukai:detail", pk=unza_id)

@require_POST
def close_toku(request, unza_id):
    unza = get_object_or_404(Unza, pk=unza_id)
    if request.user == unza.author:
        unza.toku_closed = not unza.toku_closed
        unza.save()
        messages.success(request, '投句を締め切りました。')
    else:
        messages.error(request, '投句を締め切ることができるのは句会作成者のみです。')
    return redirect("kukai:detail", pk=unza_id)

        

@login_required
def senku(request, unza_id):
    unza = get_object_or_404(Unza, pk=unza_id)
    user = request.user
    ku_set = unza.ku_set.all().values()
    ku_set = list(ku_set)
    random.shuffle(ku_set)
    return render(request, 'kukai/senku.html', {"unza": unza, "user":user, "ku_set":ku_set})

@require_POST
def save_senku(request, unza_id):
    unza = get_object_or_404(Unza, pk=unza_id)
    user = request.user
    unza.selectors.add(user)
    unza.save()
    try:
        selected_ku_list = request.POST.getlist("choice")
        # author = request.POST["author"]
    except (KeyError, unza.DoesNotExist):
        return render(request, 'kukai/detail.html', {"unza": unza, "user":user, 'error_message': '選句が有効に保存されませんでした'})
    else:
        for ku_id in selected_ku_list:
            
            ku = get_object_or_404(Ku, pk=int(ku_id))
            ku.selectors.add(user)
            ku.save()
            # ku.save()
        messages.success(request, '選句が記録されました！')
    return redirect("kukai:detail", pk=unza_id)


def close_senku(request, unza_id):
    unza = get_object_or_404(Unza, pk=unza_id)
    if request.user == unza.author:
        # unza.close_senku()
        unza.senku_closed = not unza.senku_closed
        unza.save()
        messages.success(request, '選句を締め切りました。')
    else:
        messages.error(request, '選句を締め切ることができるのは句会作成者のみです。')
    return redirect("kukai:detail", pk=unza_id)


def int2kansuji(num):
    number2kanji = ["", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
    kansuji = ""
    syo_100 = num // 100
    syo_10 = (num - 100 * syo_100) // 10
    if syo_10:
        kansuji = kansuji + (number2kanji[syo_10] if (syo_10 > 1) else "十")
    if num % 10:
        kansuji = kansuji + number2kanji[num % 10]
    elif syo_10:
        kansuji = kansuji + "十"
    return kansuji
