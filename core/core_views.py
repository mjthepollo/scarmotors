from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.forms import NumberInput, TextInput, modelformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse

from users.models import User


def login(request):
    if request.method == 'GET':
        login_form = AuthenticationForm(request)
        return render(request, "login.html", context={
            "login_form": login_form
        })
    else:
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login_user(request, user)
            return redirect(reverse("home"))
        else:
            return render(request, "login.html", context={"login_form": login_form})


@login_required
def home(request):
    return render(request, "home.html")


@login_required
def new_order(request):
    pass


@login_required
def edit_order(request):
    pass


@login_required
def finish_order(request):
    pass


@login_required
def search_orders(request):
    pass


# @login_required
# def change_goals(request):
#     period = request.GET.get("period", "short")
#     goals = Goal.get_goals_of_preiod(period)
#     goalFormsetFactory = modelformset_factory(Goal, fields=(
#         'content', 'completion_rate'), extra=0,
#         widgets={
#             'content': TextInput(
#                 attrs={'placeholder': '새로운 목표'}
#             ),
#             'completion_rate': NumberInput(
#                 attrs={'type': "range", 'class': "form-range"})})
#     if request.method == "GET":
#         goal_formset = goalFormsetFactory(queryset=goals)
#         return render(request, "change_goals.html", context={"goal_formset": goal_formset, "period": period})
#     else:
#         goal_formset = goalFormsetFactory(request.POST, queryset=goals)
#         if goal_formset.is_valid():
#             goals = goal_formset.save(commit=False)
#             for goal in goals:
#                 if goal.completion_rate == 100:
#                     goal.active = False
#                 goal.period = period
#                 goal.save()
#                 print(goal.pk, goal.content, goal.period)
#         else:
#             raise GoalException("goal_formset is not VALID")
#         if period == "short":
#             return redirect("/change_goals/?period=mid")
#         if period == "mid":
#             return redirect("/change_goals/?period=long")
#         elif period == "long":
#             return redirect("/write_diary/")


# @login_required
# def write_diary(request):
#     writing_time = Diary.get_writing_time()
#     dialogForsetInitial = Dialog.get_new_dialogs_initials(writing_time)
#     dialogFormsetFactory = modelformset_factory(Dialog, fields=(
#         'question', 'content'), extra=len(dialogForsetInitial))
#     if request.method == 'GET':
#         dialogFormset = dialogFormsetFactory(
#             initial=dialogForsetInitial, queryset=Dialog.objects.none())
#         return render(request, "write_diary.html", context={"dialogFormset": dialogFormset})
#     else:
#         dialogFormset = dialogFormsetFactory(request.POST)
#         dialogs = dialogFormset.save(commit=False)
#         diary = Diary.objects.create()
#         for dialog in dialogs:
#             dialog.diary = diary
#             dialog.save()
#         return redirect(reverse("prayer")+f"?prayer_time={writing_time}")


# @login_required
# def prayer(request):
#     prayer_time = request.GET.get("prayer_time", "morning")
#     prayer = Prayer.objects.get(prayer_time=prayer_time)
#     return render(request, "prayer.html", context={"prayer": prayer})


# @login_required
# def quote_random(request):
#     quote = Quote.objects.order_by("?").first()
#     return redirect(reverse("quote", kwargs={"pk": quote.pk}))


# @login_required
# def quote(request, pk):
#     quote = Quote.objects.get(pk=pk)
#     return render(request, "quote.html", context={"quote": quote})


# @login_required
# def quote_edit(request, pk):
#     quote = Quote.objects.get(pk=pk)
#     if request.method == "GET":
#         quoteForm = QuoteForm(instance=quote)
#         return render(request, "quote_edit.html", context={"quoteForm": quoteForm})
#     else:
#         quoteForm = QuoteForm(request.POST, instance=quote).save()
#         return redirect(f"/quote/{quote.pk}")


# @login_required
# def quote_add(request):
#     if request.method == "GET":
#         quoteForm = QuoteForm()
#         return render(request, "quote_edit.html", context={"quoteForm": quoteForm})
#     else:
#         quote = QuoteForm(request.POST).save()
#         return redirect(f"/quote/{quote.pk}")


# @login_required
# def zen(request):
#     return render(request, "static/zen.html")


# @login_required
# def principles(request):
#     return render(request, "static/principles.html")


# @login_required
# def determination(request):
#     return render(request, "static/determination.html", context={"determinations": Determination.objects.all()})
