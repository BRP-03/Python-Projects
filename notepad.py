import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog,messagebox,Menu,ttk
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
        if e.char and e.char.strip() !="":
            status[nm]=False
            self.update_header()

    def update_header(self,nm=None):
        if nm is None:
            nm = note.get() 
        if nm.startswith("new"):  
            if status[nm] == True:
                header.configure(text="My Notepad : Saved")
            else:
                header.configure(text="My Notepad : Not Saved")
        else:
            filepath = text_box[nm][1]  
            if isinstance(filepath, str):  
                if status[nm] == True:
                    header.configure(text=f"{filepath} : Saved")
                else:
                    header.configure(text=f"{filepath} : Not Saved")


class File_menu():
    def __init__(self):
        self.numbers=[]
        self.s=other_features()

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
        note.add(nm)  
        tab_frame=note._tab_dict[nm]
        txtarea=ctk.CTkTextbox(tab_frame)
        txtarea.pack(fill="both",expand=True)
        text_box[nm]=[txtarea,n]
        note.set(nm)
        self.numbers.append(n)
        status[nm]=True
        txtarea.bind("<KeyPress>",self.s.update_status)
        self.s.update_header()

    def open_file(self):
        global status,text_box
        try:
            filepath=filedialog.askopenfilename(
                title="Open File",
                filetypes=[("Text FIle","*.txt"),("All Files","*.*")]
            )
            nm=os.path.basename(filepath)
            with open(filepath,"r",encoding="utf-8") as f:
                content=f.read()
            note.add(nm)
            tab_frame=note._tab_dict[nm]
            txtarea=ctk.CTkTextbox(tab_frame)
            txtarea.pack(fill="both",expand=True)
            txtarea.insert("1.0",content)
            text_box[nm]=[txtarea,filepath]
            note.set(nm)
            status[nm]=True
            txtarea.bind("<KeyPress>",self.s.update_status)
            self.s.update_header()

        except:
            pass

    def save(self):
        global text_box,status
        if note.get()[0:3]=="new":
            filepath=filedialog.asksaveasfilename(title="Save File")
            if filepath:
                nm=note.get()
                new_nm=os.path.basename(filepath)
                txt=text_box[note.get()]
                content=txt[0].get("1.0",ctk.END)
                note.rename(nm,new_nm)
                text_box.pop(nm) 
                status.pop(nm)
                text_box[new_nm]=[txt[0],filepath]
                print(text_box)
                with open(filepath,"w") as f:
                    f.write(content)   
                note.set(new_nm)
                status[new_nm]=True
    
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
        self.s.update_header()        
    
    def save_as(self):
        global text_box, status
        filepath=filedialog.asksaveasfilename(
                title="Save File")
        if filepath:
            new_nm=os.path.basename(filepath)
            nm=note.get()
            txt=text_box[note.get()][0]
            content=txt.get("1.0",ctk.END) 
            text_box.pop(nm)
            status.pop(nm)
            text_box[new_nm]=[txt,filepath]
                  
            with open(filepath,"w") as f:
                f.write(content) 
            note.rename(nm,new_nm)
            note.set(new_nm)
            status[new_nm]=True
            self.s.update_header()

    def close(self):
        if len(text_box)==1:
            ch=self.s.check_status(note.get())
            if ch==True or ch=="saved":
                note.delete(note.get())
                text_box.clear()
                status.clear()
                self.new()
        else:
            ch=self.s.check_status(note.get())
            if ch ==True or ch=="saved":
                text_box.pop(note.get())
                note.delete(note.get())    
        self.s.update_header()

    def close_all(self):
        names=[]
        for i in note._tab_dict:
            names.append(i)

        for i in names:
            ch=self.s.check_status(i)
            if ch==True or ch=="saved":
                text_box.pop(i)
                note.delete(i)
        if len(text_box)==0:
            self.new()
        else:
            text_box.clear()
            self.new()
        self.s.update_header()

class edit_menu():
    def font_format(self):
        style = ttk.Style(win) 
        style.theme_use('default')
        style.configure('Custom.TCombobox', 
                selectbackground='#2a2a2a',
                fieldbackground='#3e3e3e',  
                background='#2a2a2a',       
                foreground='white',         
                selectforeground='white'    
               )
        top=ctk.CTkToplevel(win)
        top.geometry("300x300")
        top.title("Font Formatting")
        top.transient(win)   # Always stay on top of main window
        top.grab_set()       # Focus lock on this window
        top.focus() 
        ctk.CTkLabel(top,text="Font Family : ",font=("Arial",15,"normal")).grid(row=0,column=0,pady=10,padx=5)
        font_list = ["Arial", "Calibri", "Cambria", "Comic Sans MS", "Courier New", "Georgia",
        "Helvetica", "Impact", "Lucida Console", "MS Sans Serif", "Segoe UI","Tahoma" ,
        "Times New Roman", "Trebuchet MS", "Verdana", "TkDefaultFont", "TkFixedFont",
        "TkMenuFont", "TkTextFont", "TkHeadingFont"]
        family=ttk.Combobox(top,values=font_list,height=10,style="Custom.TCombobox")
        family.grid(row=0,column=1,pady=10,padx=5)
        frame=tk.Frame(top,height=50,width=300,bg="#232323")
        frame.grid(row=1,column=0,pady=20,columnspan=2)
        frame.grid_propagate(False)
        var=tk.StringVar()
        var.set('normal')
        ctk.CTkRadioButton(frame,text="Normal",variable=var,value="normal",font=("Arial",13),bg_color="#232323").grid(row=1,column=1)
        ctk.CTkRadioButton(frame,text="Bold",variable=var,value="bold",font=("Arial",13),bg_color="#232323").grid(row=1,column=2)
        ctk.CTkRadioButton(frame,text="Itallic",variable=var,value="italic",font=("Arial",13),bg_color="#232323").grid(row=1,column=3)
        ctk.CTkLabel(top,text="Font size ",font=("Arial",15,"normal")).grid(row=2,column=0,pady=10,padx=5)
        size=tk.StringVar()
        tk.Spinbox(top,from_=1,to=40,increment=1,textvariable=size,background="#232323",foreground="white",buttonbackground="#232323",).grid(row=2,column=1)
        size.set(13)
        def done():
            for i in text_box:
                box=note.get()
                text_box[box][0].configure(font=(family.get(),int(size.get()),var.get()))
            top.destroy()
        ctk.CTkButton(top,text="Done",font=("Arial",13,"normal"),command=done).grid(row=3,column=0,pady=10,padx=50,columnspan=2)
    
    def find_replace(self):
        # 1. Toplevel Window Setup
        top_fr = ctk.CTkToplevel(win)
        top_fr.geometry("400x250")
        top_fr.title("Find and Replace")
        top_fr.transient(win)
        top_fr.grab_set()
        top_fr.focus()
        
        # Grid layout use karenge for better alignment
        top_fr.grid_columnconfigure(1, weight=1)
        
        # 2. Find Section
        ctk.CTkLabel(top_fr, text="Find What:", font=("Arial", 14, "normal")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.find_entry = ctk.CTkEntry(top_fr, width=250)
        self.find_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # 3. Replace Section
        ctk.CTkLabel(top_fr, text="Replace With:", font=("Arial", 14, "normal")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.replace_entry = ctk.CTkEntry(top_fr, width=250)
        self.replace_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # 4. Count and Match Case Section
        self.count_label = ctk.CTkLabel(top_fr, text="Matches: 0", font=("Arial", 12, "normal"))
        self.count_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        self.match_case_var = tk.StringVar(value="off") # CTkCheckBox ke liye
        ctk.CTkCheckBox(top_fr, text="Match Case", variable=self.match_case_var, onvalue="on", offvalue="off").grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # 5. Buttons Section
        button_frame = ctk.CTkFrame(top_fr, fg_color="transparent")
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(button_frame, text="Find Next >").pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="< Find Prev").pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Replace").pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Replace All").pack(side="left", padx=5)
        
        # Objects ko instance variables mein store kar rahe hain taki dusre methods access kar sakein
        self.top_fr = top_fr
        
        # Current tab ko highlight karne ke liye initial setup
        self.s = other_features() # Assuming other_features is accessible
        
        # Hum Find and Replace ke liye ek global list of matches maintain karenge
        self.matches = [] 
        self.current_match_index = -1

# Main GUI
fm=File_menu()
of=other_features()
em=edit_menu()
win=ctk.CTk()
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
win.geometry(f"{screen_width}x{screen_height}+0+0")
header=ctk.CTkLabel(win,text="My Notepad",font=("Arial",12,"normal"))
header.pack(anchor='w')

note=ctk.CTkTabview(win,anchor="nw")
note.pack(fill="both",expand=True)
note.add("new 1")
tab_frame=note._tab_dict["new 1"]
txtarea=ctk.CTkTextbox(tab_frame)
txtarea.pack(fill="both",expand=True)
txtarea.bind("<KeyPress>",of.update_status)
text_box["new 1"]=[txtarea,1]
status["new 1"]=True
note.configure(command=of.update_header)

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
edit=Menu(menu_bar,tearoff=0,bg="gray20",fg="white",font=("Arial",10,"normal"))
menu_bar.add_cascade(label="Edit ",menu=edit)
edit.add_command(label="Font Formatting",command=em.font_format)
edit.add_command(label="Mode Dark/Light")
edit.add_command(label="Find/Replace",command=em.find_replace)
edit.add_command(label="Undo")
edit.add_command(label="Redo")

win.mainloop()