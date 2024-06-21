from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/korean_frequency_list.csv")
    to_learn = data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")  # change way sorted into dict


# ----------------------------- FUNCTIONS ------------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Korean", fill="black")  # edit text element
    canvas.itemconfig(card_word, text=current_card["Korean"], fill="black", font=("Ariel", 80, "bold"))
    canvas.itemconfig(card_bg, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    if len(current_card["English"]) > 21:
        canvas.itemconfig(card_word, font=("Ariel", 40, "bold"))
    else:
        canvas.itemconfig(card_word, font=("Ariel", 60, "bold"))
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_bg, image=card_back_img)

def is_known():
    to_learn.remove(current_card)
    save_data = pandas.DataFrame(to_learn)
    save_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Learn Korean: Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)  # adding delay; time in ms

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_bg = canvas.create_image(400, 263, image=card_front_img)  # at centre of canvas
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"), fill="black")
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 80, "bold"), fill="black")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)  # get rid of img bg colour & border
canvas.grid(row=0, column=0, columnspan=2)

cross_button_img = PhotoImage(file="images/wrong.png")
cross_button = Button(image=cross_button_img, border=0, highlightthickness=0, command=next_card)
cross_button.grid(row=1, column=0)

tick_button_img = PhotoImage(file="images/right.png")
tick_button = Button(image=tick_button_img, border=0, highlightthickness=0, command=is_known)
tick_button.grid(row=1, column=1)

# ---------------------------- MAIN PROGRAM ------------------------------- #
next_card()
window.mainloop()
