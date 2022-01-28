from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Choice, Question
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'pollapp/index.htm'
    context_object_name = 'latest_question_list'

    def get_queryset(self):

        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    
    def get_queryset(self):
        
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'pollapp/results.htm'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'pollapp/question_detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        
        return HttpResponseRedirect(reverse('pollapp:results', args=(question.id,)))