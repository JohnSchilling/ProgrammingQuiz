import random
import yaml
import pathlib
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
from string import ascii_lowercase

root = Tk()
root.title('Programming Quiz')
photo = PhotoImage(file = 'robot.png')
root.iconphoto(False, photo)
root.geometry("600x300")

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

center(root)

questionFile = 'ProgrammingVocabularyQuestions.yml'
with open(questionFile, 'r+') as file:
    data = yaml.full_load(file)
numQuestionsPerQuiz = 5

def run_quiz():
    questions = prepare_questions(numQuestionsPerQuiz)
    num_correct = 0
    
    for num, question in enumerate(questions, start=1):
        num_correct += ask_question(question)

    messagebox.showinfo("", "You got {} correct out of {} questions.".format(num_correct, num))
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
        messagebox.showinfo("", "Correct!")

        return 1
    else:
        if (numTimesCorrect != 0):
            question["numCorrect"] = numTimesCorrect - 1
        messagebox.showinfo("", "The answer is {}, not {}".format(correct_answer, answer))

        return 0

def get_answer(question, alternatives):
    buttons = []
    labels = []
    label = Label(root, text=question, wraplength=500, justify="left")
    label.pack(pady=(0,20))
    labels.append(label)
    labeled_alternatives = dict(zip(ascii_lowercase, alternatives))
    answer = StringVar()
    answer.set(' ')
    
    for label, alternative in labeled_alternatives.items():
        button = Radiobutton(root, text=alternative, variable=answer, value=label)
        button.pack(anchor=W)
        buttons.append(button)

    root.wait_variable(answer)
    answer_label = answer.get()
    for rb in buttons:
        rb.destroy()
    for lb in labels:
        lb.destroy()

    return labeled_alternatives[answer_label]

if __name__ == "__main__":
    run_quiz()
