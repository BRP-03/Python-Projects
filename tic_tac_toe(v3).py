import customtkinter as ctk 
import tkinter as tk,random,pygame,threading
from tkinter import messagebox,filedialog

def play_song(filepath):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play(-1)
    except Exception as e :
        messagebox.showerror("Error","Not able to load song.")

def choose_play():
    filepath=filedialog.askopenfilename(
        title="Select Song",
        filetypes=[("MP3 Files","*.mp3")]
    )
    if filepath:
        threading.Thread(target=play_song, args=(filepath,), daemon=True).start()

global s_mode,mode,difficulty,chance,buttons,user_move,comp_move,available_moves,winning_patterns,retry,first,play
winning_patterns,available_moves,user_move,comp_move=[[[0,0],[1,1],[2,2]],[[0,2],[1,1],[2,0]]],[],[],[]
retry=None
def replay():
    global buttons,available_moves,user_move,comp_move,retry,mode,play
    available_moves.clear()
    user_move.clear()
    comp_move.clear()
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="",state="normal",bg="white")
            available_moves.append([i,j])
    if retry is not None:
        if retry.winfo_exists():
            retry.destroy()
        retry=None
    try:
        if mode=="bot":
            # chance=random.randint(0,1)
            chance=0
            if chance==0:
                if [1,1] in available_moves:
                    buttons[1][1].config(text="O",state="disabled")
                    comp_move.append([1,1])
                    available_moves.remove([1,1])
        else:
            player_1.config(foreground="black")
            player_2.config(foreground="black")
            chance=random.randint(0,1)
            if chance==0:
                play=1
                player_1.config(foreground="yellow")
            else:
                play=2
                player_2.config(foreground="yellow")
    except:
        pass
    
def check_winner():
    global winning_patterns,user_move,comp_move,retry,mode
    for win in winning_patterns:
        u=b=0
        color_u=[]
        color_b=[]
        for x in win:
            if x in user_move:
                u+=1
                color_u.append(x)
            elif x in comp_move:
                b+=1
                color_b.append(x)
        if u==3:
            for i in color_u: 
                buttons[i[0]][i[1]].config(text="X",state="normal",bg="green")
            for i in range(3):
                for j in range(3):
                    buttons[i][j].config(state="disabled")
            retry=ctk.CTkButton(bottom_center,text="Replay",font=("Arial",20),height=7,command=replay)
            retry.grid(row=4,column=1,pady=15)
            if mode=="player":
                messagebox.showinfo("Game Over","Player 1 🎉")
            else:
                messagebox.showinfo("Game Over","You won 🎉")
            return True
        elif b==3:
            for i in color_b: 
                buttons[i[0]][i[1]].config(text="O",state="normal",bg="green")
            for i in range(3):
                for j in range(3):
                    buttons[i][j].config(state="disabled")
            retry=ctk.CTkButton(bottom_center,text="Replay",font=("Arial",20),height=7,command=replay)
            retry.grid(row=4,column=1,pady=15)
            if mode=="player":
                messagebox.showinfo("Game Over","Player 2 won 🎉")
            else:    
                messagebox.showinfo("Game Over","Bot won 🤖")
            return True
    return False

def check_draw():
    global available_moves,retry
    if not available_moves:
        retry=ctk.CTkButton(bottom_center,text="Replay",font=("Arial",20),height=7,command=replay)
        retry.grid(row=4,column=1,pady=15)
        messagebox.showinfo("Game Over","This is Draw")
        return True
    return False

def bot_game(r,c):
    global difficulty,user_move,comp_move,available_moves,winning_patterns,first
    def bot_win():
        for win in winning_patterns:
            double=[]
            ca=None
            for cell in win:
                if cell in comp_move:
                    double.append(cell)
                elif cell in available_moves:
                    ca=cell
            if len(double)==2 and ca is not None:
                r,c=ca[0],ca[1]
                buttons[r][c].config(text="O",state="disabled")
                comp_move.append(ca)
                available_moves.remove(ca)
                return False
        return True
    
    def user_block():
        for win in winning_patterns:
            double=[]
            ca=0
            for cell in win:
                if cell in user_move:
                    ca+=1
                    double.append(cell)
            if ca==2:
                for i in win:
                    if i not in double and i in available_moves:
                        r,c=i[0],i[1]
                        buttons[r][c].config(text="O",state="disabled")
                        comp_move.append([r,c])
                        available_moves.remove([r,c])
                        return False
        return True
    
    def play_opposite(r,c):
        oppose=[[[0,0],[2,2]],[[2,0],[0,2]],[[0,1],[2,1]],[[1,0],[1,2]]]
        for move in oppose:
            if [r,c] in move:
                for i in move:
                    if i in available_moves:
                        row,col=i[0],i[1]
                        buttons[row][col].config(text="O",state="disabled")
                        comp_move.append(i)
                        available_moves.remove(i)
                        return False
        return True
    def fork(first):
        if first in [[2,1],[1,0],[1,2],[0,1]]:
            if first in [[2,1],[0,1]]:
                if [2,0] in available_moves:
                    buttons[2][0].config(text="O",state="disabled")
                    comp_move.append([2,0])
                    available_moves.remove([2,0])
                else:
                    buttons[0][0].config(text="O",state="disabled")
                    comp_move.append([0,0])
                    available_moves.remove([0,0])
            else:
                if [2,0] in available_moves:
                    buttons[2][0].config(text="O",state="disabled")
                    comp_move.append([2,0])
                    available_moves.remove([2,0])
                else:
                    buttons[2][2].config(text="O",state="disabled")
                    comp_move.append([2,2])
                    available_moves.remove([2,2])
            return False
        corners = [[0,0],[0,2],[2,2],[2,0]]
        corner_strategies = {(0,0): {
            "user_block_check": [[0,2], [2,0]], # Check if user blocked cross-diagonal
            "bot_moves": [[2,2], [2,0], [0,2]] # Prioritized moves for bot
        },
        (2,2): {
            "user_block_check": [[0,2], [2,0]],
            "bot_moves": [[0,0], [2,0], [0,2]] # Prioritized moves for bot
        },
        # If player takes [0,2] or [2,0] (anti-diagonal corners)
        (0,2): {
            "user_block_check": [[0,0], [2,2]], # Check if user blocked cross-diagonal
            "bot_moves": [[2,0], [0,0], [2,2]] # Prioritized moves for bot
        },
        (2,0): {
            "user_block_check": [[0,0], [2,2]],
            "bot_moves": [[0,2], [0,0], [2,2]] }}
        first_tuple = tuple(first) 
        if first_tuple in corner_strategies:
            strategy = corner_strategies[first_tuple]
            if any(move in user_move for move in strategy["user_block_check"]):
                return True
            for r_target, c_target in strategy["bot_moves"]:
                if [r_target, c_target] in available_moves:
                    buttons[r_target][c_target].config(text="O", state="disabled")
                    comp_move.append([r_target, c_target])
                    available_moves.remove([r_target, c_target])
                    return False
        return True
    
    if len(available_moves)==9 or len(available_moves)==8:
        first=[r,c]
    
    buttons[r][c].config(text="X",state="disabled")
    available_moves.remove([r,c])
    user_move.append([r,c])
    if check_winner():
        return
    if check_draw():
        return
    if difficulty=="medium" or difficulty=="hard":
        check=bot_win()
        if check:
            check=user_block()
            if check :
                if[1,1] in available_moves:
                    buttons[1][1].config(text="O",state="disabled")
                    comp_move.append([1,1])
                    available_moves.remove([1,1])
                else:
                    if difficulty=="hard":
                        check=fork(first)
                    if check:
                        check=play_opposite(r,c)
                        if check:
                            move=random.choice(available_moves)
                            buttons[move[0]][move[1]].config(text="O",state="disabled")
                            comp_move.append(move)
                            available_moves.remove(move)
    else :
        move=random.choice(available_moves)
        buttons[move[0]][move[1]].config(text="O",state="disabled")
        comp_move.append(move)
        available_moves.remove(move)

    if check_winner():
        return
    if check_draw():
        return

def player_game(r,c):
    global play,user_move,comp_move
    if play==1:
        buttons[r][c].config(text="O",state="disabled")
        user_move.append([r,c])
        play=2
        player_2.config(foreground="yellow")
        player_1.config(foreground="black")
    else:
        buttons[r][c].config(text="X",state="disabled")
        comp_move.append([r,c])
        play=1
        player_1.config(foreground="yellow")
        player_2.config(foreground="black")
    available_moves.remove([r,c])
    if check_winner():
        return
    if check_draw():
        return    

def choose(r,c):
    global mode
    if mode=="bot":
        bot_game(r,c)
    if mode=="player":
        player_game(r,c)

def select_con(mode_):
    global s_mode,mode,chance,buttons,comp_move,available_moves,play
    if mode_=="bot":
        replay()
        player_1.config(text="Player")
        player_2.config(text="Bot")
        mode=mode_
        s_mode.destroy()
        bot_setting=ctk.CTkToplevel(win)
        bot_setting.title("")
        height,width=200,300
        win_x,win_y=win.winfo_x(),win.winfo_y()
        s_height,s_width=win.winfo_height(),win.winfo_width()
        x=win_x+(s_width/2)-(width/2)
        y=win_y+(s_height/2)-(height/2)
        bot_setting.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        bot_setting.transient(win)
        bot_setting.grab_set()
        tk.Label(bot_setting,text="Select Dificulty : ",font=("Arial",13)).grid(row=1,column=1,sticky='w')
        dif=tk.Label(bot_setting,text=" ",font=("Arial",20))
        dif.grid(row=2,column=1,columnspan=3,pady=20)
        # chance=random.randint(0,1)
        chance=0
        def set_dif(e):
            global difficulty
            if sc.get()==1 or sc.get()<=1.50:
                dif.config(text="Easy",fg="green")
                difficulty="easy"
            elif sc.get()>=1.50 and sc.get()<=2.50:
                dif.config(text="Medium",fg="orange")
                difficulty="medium"
            elif sc.get()>=2.50:
                dif.config(text="Hard",fg="red")
                difficulty="hard"
            else:
                dif.config(text="")
        sc=ctk.CTkSlider(bot_setting,from_=1,to=3,command=set_dif)
        sc.grid(row=3,column=1,columnspan=3,pady=10,padx=45)
        def check():
            if sc.get()==2.0:
                messagebox.showerror("Error","Please select difficulty level.....")
            else:
                bot_setting.destroy()
                if chance==0:
                    buttons[1][1].config(text="O",state="disabled")
                    comp_move.append([1,1])
                    available_moves.remove([1,1])
        ctk.CTkButton(bot_setting,text="Let's Play",command=check,font=("Arial",13)).grid(row=4,column=1,padx=90,pady=20)
    else:
        mode=mode_
        player_1.config(text="Player 1 (O)")
        player_2.config(text="Player 2 (X)")
        s_mode.destroy()
        chance=random.randint(0,1)
        if chance==0:
            play=1
            player_1.config(foreground="Yellow")
        else:
            play=2
            player_2.config(foreground="yellow")
        
def select_mode():
    global s_mode,mode
    s_mode=ctk.CTkToplevel(win)
    s_mode.title("")
    height,width=200,300
    win_x,win_y=win.winfo_x(),win.winfo_y()
    s_height,s_width=win.winfo_height(),win.winfo_width()
    x=win_x+(s_width/2)-(width/2)
    y=win_y+(s_height/2)-(height/2)
    s_mode.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
    s_mode.transient(win)
    s_mode.grab_set()
    ctk.CTkLabel(s_mode,text="Select Mode : ",font=("Arial",20)).grid(row=1,column=1,sticky='w')
    ctk.CTkButton(s_mode,text="Play with\nPlayer\n🧑",font=("Arial",14),command=lambda :select_con("player")).grid(row=2,column=1,pady=30,padx=5)
    ctk.CTkButton(s_mode,text="Play with\nBot\n🤖",font=("Arial",14),command=lambda:select_con("bot")).grid(row=2,column=2,padx=5)
    replay()

win=ctk.CTk()
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
win.geometry(f"{screen_width}x{screen_height}+0+0")
win.title("TIC TAC TOE")
win.update_idletasks()
win.after(100,select_mode)
ctk.set_appearance_mode("Light")
pane = tk.PanedWindow(win, orient="horizontal")
pane.pack(fill="both", expand=True)
left_frame = tk.Frame(pane, bg="lightblue", width=150)
pane.add(left_frame)
ctk.CTkButton(left_frame,text="Change\nMode",font=("Arial",13),command=select_mode).pack(pady=30)
ctk.CTkButton(left_frame,text="Change\nDifficulty",font=("Arial",13),command=lambda:select_con("bot")).pack()
ctk.CTkButton(left_frame,text="Play some \nSONG",font=("Arial",13),command=choose_play).pack(pady=30)
right_frame = tk.Frame(pane, bg="lightgreen")
pane.add(right_frame)
center = tk.Frame(right_frame, width=850, height=600)
center.pack(pady=50)
center.pack_propagate(False)  # Don't shrink to fit contents
top_center = tk.Frame(center, width=850, height=100)
top_center.pack()
top_center.pack_propagate(False)
top_center.grid_columnconfigure(0, weight=1)
top_center.grid_columnconfigure(1, weight=1)
player_1=tk.Label(top_center, text=" ", font=("Arial", 30))
player_1.grid(row=0, column=0, sticky="w", padx=105)
player_2=tk.Label(top_center, text=" ", font=("Arial", 30))
player_2.grid(row=0, column=1, sticky="e", padx=105)
bottom_center = tk.Frame(center, width=850, height=500)
bottom_center.pack(pady=60)
bottom_center.pack_propagate(False)
buttons=[]
for r in range(3):
    rows,cols,but=[],[],[]
    for c in range(3):
        btn = tk.Button(bottom_center, text="", font=("Arial", 30), width=5, height=2,command=lambda row=r,col=c:choose(row,col))
        btn.grid(row=r, column=c,pady=2)
        but.append(btn)
        available_moves.append([r,c])
        rows.append([r,c])
        cols.append([c,r])
    buttons.append(but)
    winning_patterns.append(cols)
    winning_patterns.append(rows)
    
win.mainloop()