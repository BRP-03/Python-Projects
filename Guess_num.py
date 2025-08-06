#Task 2 : Number Guesser

import tkinter as tk
from tkinter import ttk,messagebox
import tkinter.font as font
import random

def replay():
    global again
    messagebox.showinfo("Replay","Let's Play again.\nSelect range")
    guess.config(state='disabled')
    val.config(state='disabled')
    select.config(state='normal')
    again.destroy()

def num():
    global no
    if n1.get()=="" or n2.get()=="":
        messagebox.showerror("Error","Please enter some range")
        return
    if not n1.get().isnumeric() or not n2.get().isnumeric():
        messagebox.showwarning("Wrong Entry","Please enter only number")
        return
    if int(n1.get())>int(n2.get()):
        messagebox.showwarning("Wrong range","Minimum values cannot exceds Maximum value")    
        return
    if int(n1.get())==int(n2.get()):
        messagebox.showwarning("Incorrect value","Minimum and maximum value cannot be same")    
        return
    no=random.randint(int(n1.get()),int(n2.get()))
    select.config(state='disabled')
    val.config(state='normal')
    guess.config(state='normal')

def check():
    global no
    global again
    if val.get()=="":
        messagebox.showerror("Error","Please Enter a number")
        return
    if not val.get().isnumeric():
        messagebox.showwarning("Wrong entry","Please enter only number")
        return
    if int(val.get())==no:
        messagebox.showinfo("Correct","You guess correct value")
        guess.config(state='disabled')
        val.delete(0,tk.END)
        n1.set("")
        n2.set("")
        again=tk.Button(win,text="Replay",height=1,command=replay)
        again.grid(row=4,column=3,sticky='e')
    elif int(val.get())>no:
        messagebox.showinfo("Incorrect","Too high")
    else:
        messagebox.showinfo("Incorrect","Too low")

win=tk.Tk()
win.geometry("520x500")
win.title("Number Guesser")
win.config(background="lightcyan")
default=font.nametofont("TkDefaultFont")
default.config(size=13,family="Arial")
n1=tk.StringVar()
n2=tk.StringVar()
tk.Label(win,text="Enter minimum value :",bg="lightcyan").grid(row=1,column=1,sticky='w')
tk.Entry(win,textvariable=n1,font=("Arial",13),width=4).grid(row=1,column=2,sticky='w')
tk.Label(win,text="\tEnter maximum value :",bg="lightcyan").grid(row=1,column=3,sticky='w')
tk.Entry(win,textvariable=n2,font=("Arial",13),width=4).grid(row=1,column=4,sticky='w')
select=tk.Button(win,text="Select Range",font=("Arial",10),width=9,command=num)
select.grid(row=2,column=3,sticky='w',pady=20)
tk.Label(win,text="Enter number : ",bg="lightcyan",font=("Arial",15)).grid(row=3,column=1,sticky='w')
val=tk.Entry(win,width=5,font=("Arial",15),state='disabled')
val.grid(row=3,column=2)
guess=tk.Button(win,text="Guess",height=1,state='disabled',command=check)
guess.grid(row=4,column=1,sticky='w',pady=15)
win.mainloop()