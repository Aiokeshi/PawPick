from django.shortcuts import render, redirect
from catalog.models import Cards, Tag
from .models import Question, Answer
from django.shortcuts import render
from django.db.models import Count, Q
from .models import Answer, TestResult
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Question

def test_step(request, step):
    questions = Question.objects.filter(step=step)
    total_steps = Question.objects.values('step').distinct().count()

    progress = int((step / total_steps) * 100)

    if request.method == 'POST':
        answers = request.session.get('answers', {})

        
        if 'back' in request.POST:
            prev_step = step - 1 if step > 1 else 1
            return redirect('qtest:test_step', step=prev_step)

       
        for question in questions:
            answer_id = request.POST.get(f'question_{question.id}')
            if not answer_id:
                return render(request, 'qtest/test_step.html', {
                    'questions': questions,
                    'step': step,
                    'total_steps': total_steps,
                    'progress': progress,
                    'error': 'Выберите ответ'
                })

            answers[str(question.id)] = answer_id

        request.session['answers'] = answers

        next_step = step + 1

        if next_step > total_steps:
            return redirect('qtest:test_result')

        return redirect('qtest:test_step', step=next_step)

    return render(request, 'qtest/test_step.html', {
        'questions': questions,
        'step': step,
        'total_steps': total_steps,
        'progress': progress
    })

def test_result(request):
    answers_dict = request.session.get('answers', {})
    answer_ids = list(answers_dict.values())

    answers = Answer.objects.filter(id__in=answer_ids)

    tags = Tag.objects.filter(answers__in=answers).distinct()
    tag_ids = list(tags.values_list('id', flat=True))

    total_tags = len(tag_ids) if tag_ids else 1

    cards = Cards.objects.annotate(
        match_count=Count(
            'tags',
            filter=Q(tags__id__in=tag_ids),
            distinct=True
        )
    ).filter(match_count__gt=0).order_by('-match_count')

    result_cards = []
    best_card = None

    if cards.exists():
        max_match = cards.first().match_count
        cards = cards.filter(match_count=max_match)

        for card in cards:
            percent = int((card.match_count / total_tags) * 100)
            result_cards.append({
                'card': card,
                'percent': percent
            })

        best_card = cards.first()

    
    result = TestResult.objects.create(
        user=request.user if request.user.is_authenticated else None,
        best_card=best_card
    )
    result.tags.set(tags)
    result.cards.set([item['card'] for item in result_cards])

    
    request.session['answers'] = {}

    return render(request, 'qtest/result.html', {
        'results': result_cards,
        'best_card': best_card
    })

@login_required
def profile(request):
    results = TestResult.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'qtest/profile.html', {
        'results': results
    })