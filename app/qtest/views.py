from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from catalog.models import Cards
from .models import Answer, Question, TestResult, TestStep


RESULT_LIMIT = 3


def _get_step_weights():
    return dict(TestStep.objects.values_list('order', 'weight'))


def _get_total_steps():
    steps_count = TestStep.objects.count()
    if steps_count:
        return steps_count

    return Question.objects.values('step').distinct().count()


def _get_max_test_score():
    """
    Максимальный балл считается динамически:
    каждый вопрос даёт вес своего шага.
    Если тест будет заполнен по схеме 60 вопросов из описания,
    получится 144 балла.
    """
    step_weights = _get_step_weights()

    max_score = 0

    for question in Question.objects.all():
        max_score += step_weights.get(question.step, 1)

    return max_score or 1


def test_start(request):
    request.session['answers'] = {}
    return redirect('qtest:test_step', step=1)


def test_step(request, step):
    total_steps = _get_total_steps()

    if total_steps == 0:
        return render(request, 'qtest/test_step.html', {
            'questions': [],
            'step': 1,
            'total_steps': 0,
            'progress': 0,
            'step_title': 'Тест пока не заполнен',
        })

    if step < 1:
        return redirect('qtest:test_step', step=1)

    if step > total_steps:
        return redirect('qtest:test_result')

    step_object = TestStep.objects.filter(order=step).first()

    questions = list(
        Question.objects
        .filter(step=step)
        .prefetch_related('answers__tag')
        .order_by('order')
    )

    progress = int((step / total_steps) * 100)

    saved_answers = request.session.get('answers', {})

    for question in questions:
        question.selected_answer_id = int(saved_answers.get(str(question.id), 0) or 0)

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
                    'step_title': step_object.title if step_object else f'Шаг {step}',
                    'error': 'Выберите ответ на каждый вопрос этого шага.',
                })

            answer_exists = Answer.objects.filter(
                id=answer_id,
                question=question
            ).exists()

            if not answer_exists:
                return render(request, 'qtest/test_step.html', {
                    'questions': questions,
                    'step': step,
                    'total_steps': total_steps,
                    'progress': progress,
                    'step_title': step_object.title if step_object else f'Шаг {step}',
                    'error': 'Выбран некорректный вариант ответа.',
                })

            answers[str(question.id)] = answer_id

        request.session['answers'] = answers
        request.session.modified = True

        next_step = step + 1

        if next_step > total_steps:
            return redirect('qtest:test_result')

        return redirect('qtest:test_step', step=next_step)

    return render(request, 'qtest/test_step.html', {
        'questions': questions,
        'step': step,
        'total_steps': total_steps,
        'progress': progress,
        'step_title': step_object.title if step_object else f'Шаг {step}',
    })


def test_result(request):
    answers_dict = request.session.get('answers', {})

    if not answers_dict:
        return redirect('qtest:test_step', step=1)

    answer_ids = list(answers_dict.values())

    selected_answers = (
        Answer.objects
        .filter(id__in=answer_ids, tag__isnull=False)
        .select_related('tag', 'question')
    )

    step_weights = _get_step_weights()
    max_test_score = _get_max_test_score()

    user_tag_scores = defaultdict(int)

    for answer in selected_answers:
        user_tag_scores[answer.tag_id] += step_weights.get(answer.question.step, 1)

    card_results = []

    for card in Cards.objects.prefetch_related('tags').all():
        score = 0

        for tag in card.tags.all():
            score += user_tag_scores.get(tag.id, 0)

        if score <= 0:
            continue

        percent = round(score / max_test_score * 100)

        card_results.append({
            'card': card,
            'score': score,
            'percent': min(percent, 100),
        })

    card_results.sort(key=lambda item: item['score'], reverse=True)
    card_results = card_results[:RESULT_LIMIT]

    best_card = card_results[0]['card'] if card_results else None
    total_score = card_results[0]['score'] if card_results else 0

    result = TestResult.objects.create(
        user=request.user if request.user.is_authenticated else None,
        best_card=best_card,
        total_score=total_score,
    )

    result.tags.set(user_tag_scores.keys())
    result.cards.set([item['card'] for item in card_results])

    request.session['answers'] = {}
    request.session.modified = True

    return render(request, 'qtest/result.html', {
        'results': card_results,
        'best_card': best_card,
        'max_test_score': max_test_score,
    })

@login_required
def profile(request):
    max_test_score = _get_max_test_score()

    results = list(
        TestResult.objects
        .filter(user=request.user)
        .select_related('best_card')
        .prefetch_related('cards')
        .order_by('-created_at')
    )

    for result in results:
        result.percent = min(round(result.total_score / max_test_score * 100), 100)

        similar_cards = list(result.cards.all())

        if result.best_card:
            similar_cards = [
                card for card in similar_cards
                if card.id != result.best_card.id
            ]

        result.similar_cards = similar_cards[:2]

    return render(request, 'qtest/profile.html', {
        'results': results,
        'favorite_count': request.user.favorite_cards.count(),
    })
