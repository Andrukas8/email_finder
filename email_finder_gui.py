from tkinter import *
window = Tk()
window.title("Email Finder")
window.geometry("500x500")

entry = Entry(window,
              font=("Arial", 10),
              width=60
              )
entry.grid(row=0, column=0, columnspan=3)

search_button = Button(window, text="Search", font=("Arial", 10))
search_button.grid(row=1, column=0)

stop_button = Button(window, text="Stop", font=("Arial", 10))
stop_button.grid(row=1, column=2)

close_button = Button(window, text="Close", font=("Arial", 10))
close_button.grid(row=1, column=1)

results = Text(window,
               font=("Arial", 10),
               height=10,
               width=25,
               padx=0,
               pady=0,
               )
results.grid(row=2, column=0, columnspan=3)

window.mainloop()
