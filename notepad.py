import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog,messagebox,Menu
import os

global text_box,status
text_box={}
status={}

class other_features():
    global status
    def check_status(self,nm):
        if status[nm]==False:
            ch=messagebox.askyesno("Warning",f"{nm} file is not yet save. Do you want to close the file ? ")
            return ch
        else:
            return "saved"

    def update_status(self,e):
        nm=note.get()
        status[nm]=False
        self.on_tab_change(note.get())

    def on_tab_change(self,nm):
        lis=text_box[nm]
        state=status[nm]
        if nm[0:3]!="new":
            print("C1")
            if state==True:
                print("C2")
                header.configure(text=f"{lis[1]} : Saved")
            else:
                header.configure(text=f"{lis[1]} : Not Saved")
        else:
            header.configure(text="My Notepad")

class File_menu():
    def __init__(self):
        self.numbers=[]
    s=other_features()

    def new(self):
        global text_box,status
        self.numbers.clear()
        for i in text_box:
            lis=text_box[i]
            if type(lis[1]) is int:
                if lis[1] not in self.numbers:
                    self.numbers.append(lis[1]) 
        
        self.numbers.sort()
        if len(self.numbers)!=1:
            if len(self.numbers)==0:
                n=1
            else:
                n=None
                if self.numbers[0]!=1:
                    n=1
                else:
                    i=0
                    while i<len(self.numbers):
                        j=i+1
                        if j==len(self.numbers):
                            break
                        else:
                            if self.numbers[i]+1!=self.numbers[j]:
                                n=self.numbers[i]+1
                                break
                        i+=1
                    if n==None:
                        n=self.numbers[len(self.numbers)-1]+1
        else:
            n=2
        
        nm=f"new {n}"
        new_tab=note.add(nm)  
        txtarea=ctk.CTkTextbox(new_tab)
        txtarea.pack(fill="both",expand=True)
        text_box[nm]=[txtarea,n]
        print(text_box)
        note.set(nm)
        self.numbers.append(n)
        txtarea.bind("<KeyPress>",self.s.update_status)
        status[nm]=True
        self.s.on_tab_change(note.get())

    def open_file(self):
        global status
        try:
            filepath=filedialog.askopenfilename(
                title="Open File",
                filetypes=[("Text FIle","*.txt"),("All Files","*.*")]
            )
            nm=os.path.basename(filepath)
            with open(filepath,"r",encoding="utf-8") as f:
                content=f.read()
            new_tab=note.add(nm)
            txtarea=ctk.CTkTextbox(new_tab)
            txtarea.pack(fill="both",expand=True)
            txtarea.insert("1.0",content)
            text_box[nm]=[txtarea,filepath]
            print(text_box)
            note.set(nm)
            status[nm]=True
            txtarea.bind("<KeyPress>",self.s.update_status)
            self.s.on_tab_change(note.get())
        except:
            pass

    def save(self):
        if note.get()[0:3]=="new":
            filepath=filedialog.asksaveasfilename(title="Save File")
            if filepath:
                nm=note.get()
                new_nm=os.path.basename(filepath)

                txt=text_box[note.get()]
                content=txt[0].get("1.0",ctk.END)
                text_box.pop(nm) 
                text_box[new_nm]=[txt[0],filepath]
                print(text_box)
                note.rename(nm,new_nm)
                with open(filepath,"w") as f:
                    f.write(content)   
                note.set(new_nm)
                status.pop(nm)
                status[new_nm]=True
                print(text_box)
                self.s.on_tab_change(note.get())
        else:
            txt=text_box[note.get()]
            content=txt[0].get("1.0",ctk.END) 
            filepath=txt[1]
            
            with open(filepath,"w") as f:
                f.write(content)
            note.set(os.path.basename(filepath))	
            for i in status:
                if i==note.get():
                    status[i]=True
            print(text_box)
            self.s.on_tab_change(note.get())
    
    def save_as(self):
        filepath=filedialog.asksaveasfilename(
                title="Save File"    )
        if filepath:
            new_nm=os.path.basename(filepath)
            nm=note.get()
            txt=text_box[note.get()]
            content=txt[0].get("1.0",ctk.END) 
            text_box.pop(nm)
            text_box[new_nm]=[txt[0],filepath]
                  
            with open(filepath,"w") as f:
                f.write(content) 
            note.rename(nm,new_nm)
            note.set(new_nm)
            status.pop(nm)
            status[new_nm]=True
            print(text_box)
            self.s.on_tab_change(note.get())

    def close(self):
        if len(text_box)==1:
            ch=self.s.check_status(note.get())
            if ch==True or ch=="saved":
                note.delete(note.get())
                text_box.clear()
                status.clear()
                self.new()
                print(text_box)
        else:
            ch=self.s.check_status(note.get())
            if ch ==True or ch=="saved":
                text_box.pop(note.get())
                note.delete(note.get())    
            print(text_box)

    def close_all(self):
        names=[]
        for i in note._tab_dict:
            names.append(i)

        for i in names:
            ch=self.s.check_status(i)
            if ch==True or ch=="saved":
                text_box.pop(i)
                note.delete(i)
        print(text_box)
        if len(text_box)==0:
            self.new()
        else:
            text_box.clear()
            self.new()

# Main GUI
fm=File_menu()
of=other_features()
win=ctk.CTk()
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
win.geometry(f"{screen_width}x{screen_height}+0+0")
header=ctk.CTkLabel(win,text="My Notepad",font=("Arial",12,"normal"))
header.pack(anchor='w')

note=ctk.CTkTabview(win,anchor="nw")
note.pack(fill="both",expand=True)
note._segmented_button.configure(command=of.on_tab_change)
new_tab=note.add("new 1")
txtarea=ctk.CTkTextbox(new_tab)
txtarea.pack(fill="both",expand=True)
text_box["new 1"]=[txtarea,1]
status["new 1"]=True
txtarea.bind("<KeyPress>",of.update_status)

menu_bar=Menu(win,bg="gray20",fg="white",font=("Arial",10,"normal"))
win.config(menu=menu_bar)
file_menu=Menu(menu_bar,tearoff=0,bg="gray20",fg="white",font=("Arial",10,"normal"))
menu_bar.add_cascade(label="File",menu=file_menu)
file_menu.add_command(label="New         ( Ctrl+N )",command=fm.new)
file_menu.add_command(label="Open        ( Ctrl+O )",command=fm.open_file)
file_menu.add_command(label="Save        ( Ctrl+S )",command=fm.save)
file_menu.add_command(label="Save As     ( Ctrl+Shift+S )",command=fm.save_as)
file_menu.add_command(label="Close       ( Ctrl+W )",command=fm.close)
file_menu.add_command(label="Close All   ( Ctrl+Shift+W )",command=fm.close_all)
file_menu.add_command(label="Exit        ( Alt+F4 )",command=quit)
edit_menu=Menu(menu_bar,tearoff=0,bg="gray20",fg="white",font=("Arial",10,"normal"))
menu_bar.add_cascade(label="Edit ",menu=edit_menu)
edit_menu.add_cascade(label="Font Formatting")
edit_menu.add_cascade(label="Mode Dark/Light")
edit_menu.add_cascade(label="Finding")
edit_menu.add_cascade(label="Undo")
edit_menu.add_cascade(label="Redo")

win.mainloop()