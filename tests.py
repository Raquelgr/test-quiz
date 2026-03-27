import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_choice_ids():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')

    ids = [choice.id for choice in question.choices]
    assert ids == [1, 2, 3]

def test_remove_choice():
    question = Question(title='q1')
    question.add_choice('a')
    choice_b = question.add_choice('b')

    question.remove_choice_by_id(choice_b.id)

    assert len(question.choices) == 1
    assert question.choices[0].text == 'a'

def test_remove_choice_with_invalid_id():
    question = Question(title='q1')
    question.add_choice('a')

    with pytest.raises(Exception):
        question.remove_choice_by_id(999)

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    question.remove_all_choices()
    assert len(question.choices) == 0

def test_set_correct_choices():
    question = Question(title='q1', max_selections=2)
    choice_a = question.add_choice('a')
    choice_b = question.add_choice('b')
    question.add_choice('c')

    question.set_correct_choices([choice_a.id, choice_b.id])

    assert choice_a.is_correct
    assert choice_b.is_correct
    assert not question.choices[2].is_correct

def test_correct_selected_choices():
    question = Question(title='q1', max_selections=2)
    choice_a = question.add_choice('a')
    choice_b = question.add_choice('b')
    question.set_correct_choices([choice_a.id])

    result = question.correct_selected_choices([choice_a.id, choice_b.id])
    assert result == [choice_a.id]

def test_correct_selected_choices_exceeding_max_selections():
    question = Question(title='q1', max_selections=1)
    choice_a = question.add_choice('a')
    choice_b = question.add_choice('b')

    with pytest.raises(Exception):
        question.correct_selected_choices([choice_a.id, choice_b.id])

def test_add_choice_with_invalid_text():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.add_choice('')
    with pytest.raises(Exception):
        question.add_choice('a' * 101)

def test_correct_selected_choices_with_no_correct_answer():
    question = Question(title='q1')
    choice_a = question.add_choice('a')
    question.add_choice('b')

    result = question.correct_selected_choices([choice_a.id])
    assert result == []