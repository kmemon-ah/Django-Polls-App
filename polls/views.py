from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from .models import Question,Choice
from django.urls import reverse
# from django.template import loader
from django.db.models import F
from django.urls import reverse
from django.views import generic


# Create your views here.

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date') [:5]
#     # template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list':latest_question_list,
#     }
#     # return HttpResponse (template.render(context,request))
#     return render(request, 'polls/index.html', context)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    # def get_quet(self):
    #     question = get_object_or_404(Question,pk=question_id)
    #     return render(request,'polls/detail.html', {'question':question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# def detail(request,question_id):
#     return HttpResponse("You are looking at question %s." %question_id)

# def results(request,question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request,'polls/results.html',{'question':question})


def vote (request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_message':"You didn't select a choice",
        })
    else:
        # selected_choice.votes += 1 --can occur race condition
        selected_choice.votes= F('votes') + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# def detail(request,question_id):
#     try:
#         question = Question.object.get(pk=question_id)
#     except:
#         raise Http404("Question Does Not Exist")
#     return render(request,'polls/detail.html', {'question':question})

# def detail(request,question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request,'polls/detail.html', {'question':question})


