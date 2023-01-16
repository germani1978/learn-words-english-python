import random
from tkinter import *
import pandas

BK = '#B1DDC6'
to_learn = {}
try:
    data = pandas.read_csv('./data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pandas.read_csv('./data/all_word.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')

current_card = {}

#ACTION
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title,text='English',fill='black')
    canvas.itemconfig(card_word,text=current_card['english'],fill='black')
    canvas.itemconfig(card_background, image=card_front )
    flip_timer = window.after(3000, func=flip_card)
    
def is_known():
    to_learn.remove(current_card)
    next_card()
    data = pandas.DataFrame(to_learn)
    data.to_csv('./data/words_to_learn.csv',index=False)

def flip_card():
    canvas.itemconfig(card_title,text='Spanish',fill='white')
    canvas.itemconfig(card_word,text=current_card['spanish'],fill='white')
    canvas.itemconfig(card_background, image=card_back )
    
    

#UI
window = Tk()
window.title('English')
window.config(padx=50, pady=50, bg=BK)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_back = PhotoImage(file='images/card_back.png')
card_front = PhotoImage(file='images/card_front.png')

card_background=canvas.create_image(400,263,image=card_front)
card_title = canvas.create_text(400, 150, text='', font=('Ariel', 40, 'italic'))
card_word = canvas.create_text(400, 263, text='', font=('Ariel', 60, 'bold'))
canvas.config(bg=BK, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file='./images/wrong.png')
unknown_button = Button(image=cross_image,highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file='./images/right.png')
known_button = Button(image=check_image,highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()




window.mainloop()