from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
try:
  data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
  original_data = pandas.read_csv("french_words.csv")
  to_learn = original_data.to_dict(orient="records")
else:
  to_learn = data.to_dict(orient="records")



def next_card():
  global current_card,flip_timer
  window.after_cancel(flip_timer)
  current_card = random.choice(to_learn)
  canvas.itemconfig(card_title,text="French",fill="black")
  canvas.itemconfig(card_word,text=current_card["French"],fill="black")
  canvas.itemconfig(card_background,image=card_front_image)
  flip_timer = window.after(3000,func=flip_card)



def flip_card():
    if "English" in current_card:  # Check if the key exists
      canvas.itemconfig(card_title,text="English",fill="white")
      canvas.itemconfig(card_word,text=current_card["English"],fill ="white")
    else:
      # Handle the case where "English" is missing (e.g., display an error message)
      canvas.itemconfig(card_word, text="No English available", fill="white")
    canvas.itemconfig(card_background,image=card_back_image)

def is_known():
  global to_learn
  if current_card in to_learn:  # Check if the card is in the list
      to_learn.remove(current_card)
      data = pandas.DataFrame(to_learn)
      data.to_csv("words_to_learn.csv",index=False)
      next_card()
  else:
      # Handle the case where the card is not in the list (e.g., display a message)
      print("Card not found in to_learn")

# Window setup
window = Tk()
window.title("Flashy")
window.config(padx=10,pady=10,bg=BACKGROUND_COLOR)

flip_timer = window.after(3000,func=flip_card)

canvas = Canvas(width=800,height=526)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400,263,image=card_front_image)
card_title=canvas.create_text(400,150,text="Title",font=("Arial",30,"italic"))
card_word = canvas.create_text(400,263,text="Word",font=("Arial",50,"bold"))
canvas.config(bg=BACKGROUND_COLOR,highlightthickness=0)
canvas.grid(column=0,row=0,columnspan=2)


# unknown button
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image,highlightthickness=0,command=next_card)
unknown_button.grid(column=0,row=1)

# known button
right_image = PhotoImage(file="images/right.png")
known_button = Button(image=right_image,highlightthickness=0,command=is_known)
known_button.grid(column=1,row=1)









window.mainloop()

