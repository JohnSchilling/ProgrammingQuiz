import random
import yaml
import pathlib
from tkinter import *
from PIL import ImageTk,Image
from string import ascii_lowercase

root = Tk()
root.title('Frame Test')
photo = PhotoImage(file = 'robot.png')
root.iconphoto(False, photo)
answerLabels = []

questionFile = 'ProgrammingVocabularyQuestions.yml'
with open(questionFile, 'r+') as file:
    data = yaml.full_load(file)
numQuestionsPerQuiz = 5

def run_quiz():
    questions = prepare_questions(numQuestionsPerQuiz)
    num_correct = 0
    
    for num, question in enumerate(questions, start=1):
        #print(f"\nQuestion {num}:")
        num_correct += ask_question(question)

    for lb in answerLabels:
        lb.destroy()

    label = Label(root, text="You got {num_correct} correct out of {num} questions")
    label.pack()
    #print(f"\nYou got {num_correct} correct out of {num} questions")
    f = open(questionFile,'w')
    yaml.dump(data, f)
    f.close()

def prepare_questions(numQuestions):
    questions = []
    
    for item in data:
        questions.append(item)

    filteredQuestions = check_questions(questions)
    num_questions = min(numQuestions, len(filteredQuestions))
    
    return random.sample(filteredQuestions, k=num_questions)
    
def check_questions(questions):
    filteredQuestions = []
    
    for question in questions:
        if question["numCorrect"] != 5:
            filteredQuestions.append(question)
    
    return filteredQuestions

def ask_question(question):
    correct_answer = question["answer"]
    alternatives = [question["answer"]] + question["alternatives"]
    ordered_alternatives = random.sample(alternatives, k=len(alternatives))
    answer = get_answer(question["question"], ordered_alternatives)
    numTimesCorrect = question["numCorrect"]

    if answer == correct_answer:
        if (numTimesCorrect != 5):
            question["numCorrect"] = numTimesCorrect + 1
        label = Label(root, text="Correct!")
        label.pack()
        answerLabels.append(label)
        #print("Correct!")
        return 1
    else:
        if (numTimesCorrect != 0):
            question["numCorrect"] = numTimesCorrect - 1
        #print(f"The answer is {correct_answer!r}, not {answer!r}")
        label = Label(root, text="The answer is {correct_answer}, not {answer}")
        label.pack()
        answerLabels.append(label)
        return 0

def get_answer(question, alternatives):
    #print(f"{question}")
    buttons = []
    labels = []
    label = Label(root, text=question)
    label.pack()
    labels.append(label)
    labeled_alternatives = dict(zip(ascii_lowercase, alternatives))
    answer = StringVar()
    answer.set(' ')
    for label, alternative in labeled_alternatives.items():
        #print(f"  {label}) {alternative}")
        button = Radiobutton(root, text=alternative, variable=answer, value=label)
        button.pack(anchor=W)
        buttons.append(button)

    root.wait_variable(answer)
    #answer_label = input("\nChoice? ")
    answer_label = answer.get()
    for rb in buttons:
        rb.destroy()
    for lb in labels:
        lb.destroy()
    #while answer_label not in labeled_alternatives:
        #print(f"Please answer one of {', '.join(labeled_alternatives)}")

    return labeled_alternatives[answer_label]

if __name__ == "__main__":
    run_quiz()
