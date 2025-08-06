import customtkinter as ctk

global flag,neg,mem
flag=True
neg=0
mem=[]
def check(val):
    global flag,neg,mem  
    if len(entry.get())==0 and val.isdigit():
        entry.insert(ctk.END,val)
    else:
        if not val.isdigit() and len(entry.get())!=0 :
            if entry.get()[-1].isdigit():
                if val=="." and flag:
                    entry.insert(ctk.END,val)
                    flag=False
                elif val!=".":
                    entry.insert(ctk.END,val)
                    flag=True
                    neg=0
                    mem=[]
        elif val.isdigit():
            entry.insert(ctk.END,val)
    
def negative():
    if len(entry.get())==0:
        return
    global neg,mem
    try:
        if float(entry.get())<0:
            x=float(entry.get())
            y=x*-2
            x=x+y
            entry.delete(0,ctk.END)
            if x.is_integer():
                entry.insert(ctk.END,int(x))
            else:
                entry.insert(ctk.END,x)
            neg=0
            mem=[]
            return
    except :
        pass
    if neg==0:
        exp=entry.get()
        i=len(exp)-1
        char=""
        for op in reversed(exp):
            if op.isdigit() or op==".":
                char=op+char
                i-=1
            elif op in ['/','-','+','%','*']:
                break
        mem.append(i+1)
        mem.append(char)
        ch="-"+char
        neg=1
        i+=1
        entry.delete(i,ctk.END)
        entry.insert(ctk.END,ch)
    elif neg==1:
        entry.delete(mem[0],ctk.END)
        entry.insert(ctk.END,mem[1])
        neg=0
        mem=[]

def calulation(exp):
    stack,postfix=[],[]
    def pre(op):
        if op in ['-','+']:
            return 1
        if op in ['%','/','*']:
            return 2
        return 0
    
    def all_in():
        i=len(stack)-1
        while i>=0:
            if stack[i]=="(":
                stack.pop(i)
                return
            else:
                postfix.append(stack[i])
                stack.pop(i)
            i-=1
    
    def check(op):
        if len(stack)==0:
            stack.append(op)
            return
        if pre(stack[-1])>=pre(op):
            postfix.append(stack[-1])
            stack.pop(len(stack)-1)
            check(op)
        else:
            stack.append(op)
            return

    infix=["("]+exp+[")"]
    for op in infix:
        if type(op) is float:
            postfix.append(op)  
            continue
        if op =="(":
            stack.append(op)
        elif op in ['+','-','/','*','%']:
            check(op)
        elif op==")":
            all_in()
    def post_to_sol(exp1):
        sol=[]
        for op in exp1:
            if op not in ['-','/','+','*','%']:
                sol.append(op)
            elif op in ['+','-','/','*','%'] and len(sol)>=2:
                b,a=sol.pop(),sol.pop()
                if   op=="+":sol.append(a+b)
                elif op=="-":sol.append(a-b)
                elif op=="*":sol.append(a*b)
                elif op=="/":
                    if a==0 or b==0:
                        sol.append("ERROR")
                    else:
                        sol.append(a/b)
                elif op=="%":sol.append(a%b)
        return sol[0]
    sol=post_to_sol(postfix)
    entry.delete(0,ctk.END)
    if type(sol) is not str:
        if sol.is_integer():
            sol=int(sol)
    entry.insert(ctk.END,sol)

def calc(exp):
    if len(entry.get())==0 :
        return
    global mem,neg
    mem=[]
    neg=0
    tokens=[]
    char=""
    flag=True
    char+=exp[0]
    for op in exp[1:len(exp)]:
        if op.isdigit() :
            char+=op
            flag=True
        elif op==".":
            if char and "." not in char:
                char+=op
        elif op=="-" and not flag and not char:
            char+=op
            flag=True
        elif op in ['-','/','+','*','%']:
            flag=False
            tokens.append(char)
            tokens.append(op)
            char=""
    if char:
        tokens.append(char)
        char=""
    token=[]
    for i in tokens:
        if i in ['/','-','+','%','*']:
            token.append(i)
        else:
            x=float(i)
            token.append(x)
    calulation(token)
        
def key_event(event):
    key = event.char
    if key.isdigit(): 
        check(key)
    elif key in ['+', '-', '*', '/', '%',"."]:
        check(key)
    elif key == '\r': 
        calc(entry.get())  
    elif key == '\x08': 
        if entry.get():
            entry.delete(len(entry.get())-1, ctk.END)

win=ctk.CTk()
win.geometry("320x400")
win.title("Calculator")

entry=ctk.CTkEntry(win,height=50,width=300,font=("Arial",25),justify="right")
entry.grid(row=0,column=0,columnspan=4,pady=20)

btn_r=ctk.CTkButton(win,text="-/+",height=50,width=72,corner_radius=50,font=("Arial",20),command=lambda :negative())
btn_r.grid(row=1,column=0,pady=4,padx=2)  
btn_C=ctk.CTkButton(win,text="C",height=50,width=72,corner_radius=50,font=("Arial",23),command=lambda :entry.delete(0,ctk.END))
btn_C.grid(row=1,column=1,pady=4,padx=2)
btn_x=ctk.CTkButton(win,text="⌫",height=50,width=72,corner_radius=50,font=("Arial",20),command=lambda:entry.delete(len(entry.get())-1,ctk.END))
btn_x.grid(row=1,column=2,pady=4,padx=2)
btn_eq=ctk.CTkButton(win,text="=",height=50,width=72,corner_radius=50,font=("Arial",23),command=lambda :calc(entry.get()))
btn_eq.grid(row=1,column=3,pady=4,padx=2)

i=1
for j in range(2,5):
    for k in range(3):
        btn=ctk.CTkButton(win,text=i,height=50,width=72,corner_radius=50,font=("Arial",23),command=lambda val=i:check(str(val)))
        btn.grid(row=j,column=k,pady=4,padx=2)
        i+=1

btn_plus=ctk.CTkButton(win,text="+",height=50,width=72,corner_radius=50,font=("Arial",23),command=lambda val="+":check(val))
btn_plus.grid(row=2,column=3,pady=4,padx=2)
btn_minus=ctk.CTkButton(win,text="-",height=50,width=72,corner_radius=50,font=("Arial",23),command=lambda val="-":check(val))
btn_minus.grid(row=3,column=3,pady=4,padx=2)
btn_multi=ctk.CTkButton(win,text="*",height=50,width=72,corner_radius=50,font=("Arial",23),command=lambda val="*":check(val))
btn_multi.grid(row=4,column=3,pady=4,padx=2)
btn_0=ctk.CTkButton(win,text="0",height=50,width=72,corner_radius=50,font=("Arial",23),command=lambda val="0":check(str(val)))
btn_0.grid(row=5,column=0,pady=4,padx=2)
btn_00=ctk.CTkButton(win,text=".",height=50,width=72,corner_radius=50,font=("Arial",23),command=lambda val=".":check(val))
btn_00.grid(row=5,column=1,pady=4,padx=2)
btn_modu=ctk.CTkButton(win,text="%",height=50,width=72,corner_radius=50,font=("Arial",23),command=lambda val="%":check(val))
btn_modu.grid(row=5,column=2,pady=4,padx=2)
btn_div=ctk.CTkButton(win,text="/",height=50,width=72,corner_radius=50,font=("Arial",23),command=lambda val="/":check(val))
btn_div.grid(row=5,column=3,pady=4,padx=2)  

win.bind("<Key>",key_event)
win.mainloop()