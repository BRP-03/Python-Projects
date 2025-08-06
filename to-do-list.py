import customtkinter as ctk
import datetime,json,uuid
from tkinter import messagebox
import tkinter as tk 
from plyer import notification
from apscheduler.schedulers.background import BackgroundScheduler

global today,entry

def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name='To-Do List'
    )

# settings.json file ko load karo
def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Default settings
        return {"notification_enabled": True, "end_of_day_time": "23:00"}

# settings ko save karo
def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)

global_settings = load_settings()

def send_end_of_day_notification():
    # settings.json se current settings load karo
    settings = load_settings()
    if not settings["notification_enabled"]:
        return

    all_tasks = []
    try:
        with open("to_do_list_task.json", "r") as f:
            all_tasks = json.load(f)
    except:
        return

    today_date = datetime.date.today().strftime("%m/%d/%y")
    pending_tasks = [
        task["task_name"] for task in all_tasks
        if not task["completed"] and task["due_date"] == today_date
    ]

    if pending_tasks:
        message = "Aapke aaj ke pending tasks hain:\n" + "\n".join(pending_tasks)
        show_notification(
            title="End of Day Reminder",
            message=message
        )

def settings_menu():
    global global_settings
    
    settings_win = ctk.CTkToplevel(win)
    settings_win.title("Notification Settings")
    settings_win.geometry("300x200")
    settings_win.transient(win)
    settings_win.grab_set()

    # Function to save settings when changes are made
    def apply_settings():
        global_settings["notification_enabled"] = notification_checkbox.get()
        global_settings["end_of_day_time"] = time_combobox.get()
        save_settings(global_settings)
        settings_win.destroy()
        
        # Scheduler ko update karo
        update_scheduler_job()

    # Function to update the cron job
    def update_scheduler_job():
        # Purana cron job remove karo
        for job in scheduler.get_jobs():
            if job.id == 'end_of_day_job':
                job.remove()
                
        # Agar notifications enabled hain, to naya job schedule karo
        if global_settings["notification_enabled"]:
            hour, minute = global_settings["end_of_day_time"].split(":")
            scheduler.add_job(
                send_end_of_day_notification,
                'cron',
                hour=hour,
                minute=minute,
                id='end_of_day_job'
            )

    # UI for Notification Enable/Disable
    # UI for Notification Enable/Disable
    ctk.CTkLabel(settings_win, text="Enable Notifications:").pack(pady=10)
    notification_checkbox = ctk.CTkCheckBox(settings_win, text="", onvalue=True, offvalue=False)
    notification_checkbox.pack()

# Sahi tareeke se checkbox ki state set karein
    if global_settings["notification_enabled"]:
        notification_checkbox.select()
    else:
        notification_checkbox.deselect()

    # UI for End-of-Day Time
    ctk.CTkLabel(settings_win, text="End of Day Reminder Time:").pack(pady=10)
    time_options = [f"{h:02d}:00" for h in range(24)]
    time_combobox = ctk.CTkComboBox(settings_win, values=time_options)
    time_combobox.pack()
    time_combobox.set(global_settings["end_of_day_time"])
    
    # Save button
    save_button = ctk.CTkButton(settings_win, text="Save Settings", command=apply_settings)
    save_button.pack(pady=20)

def set_date():
    global date,time
    def setdt():
        global date,time
        time_str="23:59"
        if month.get()==" " or Date.get()==" " :
            messagebox.showerror("Error","Please select date and time properly")
        else:
            x=f"{month.get()}/{Date.get()}/25"
            plan_date=datetime.datetime.strptime(x,"%m/%d/%y").date().strftime("%m/%d/%y")
            
            if hr.get()==" " or min_.get()==" ":
                plan_time=datetime.datetime.strptime(time_str,"%H:%M").time()
            else:
                plan_time=datetime.time(int(hr.get()),int(min_.get()))
        date=plan_date
        time=plan_time
        select_date_time.destroy()
    
    select_date_time=ctk.CTkToplevel(win)
    height_,width_=150,300
    s_height,s_width=planned_sec.winfo_height(),planned_sec.winfo_width()
    win_x,win_y=planned_sec.winfo_x(),planned_sec.winfo_y()
    x=win_x+(s_width-300)-(width_-250)
    y=win_y+(s_height-300)-(height_-250)
    select_date_time.geometry(f"{width_}x{height_}+{int(x)}+{int(y)}")
    select_date_time.transient(win)
    select_date_time.grab_set()
    ctk.CTkLabel(select_date_time,text="Hr :",font=("Calibri",20)).grid(row=0,column=0,sticky='w')
    time_hr=[' ','00' ,'01' ,'02' ,'03' ,'04' ,'05' ,'06' ,'07' ,'08' ,'09' ,'10',
                '11','12','13','14','15','16','17','18','19','20','21','22','23']
    time_min=[' ','01','02','03','04','05','06','07','08','09','10',
                '11','12','13','14','15','16','17','18','19','20',
                '21','22','23','24','25','26','27','28','29','30',
                '31','32','33','34','35','36', '37','38','39','40',
                '51','42','43','44','45','46','47','48','49','50',
                '51','52','53','54','55','56','57','58','59']
    hr=ctk.CTkComboBox(select_date_time,width=60,values=time_hr,height=30)
    hr.grid(row=0,column=1,padx=10,sticky='e')
    ctk.CTkLabel(select_date_time,text="Min :",font=("Calibri",20)).grid(row=0,column=2,sticky='w')
    min_=ctk.CTkComboBox(select_date_time,width=60,values=time_min,height=30)
    min_.grid(row=0,column=3,padx=10,sticky='e')
    mon=[' ',"01","02","03","04","05","06","07","08","09","10","11","12"]
    dt=[' ','01','02','03','04','05','06','07','08','09','10',
                '11','12','13','14','15','16','17','18','19','20',
                '21','22','23','24','25','26','27','28','29','30',
                '31']
    ctk.CTkLabel(select_date_time,text="Month :",font=("Calibri",20)).grid(pady=20,row=1,column=0,sticky='w')
    month=ctk.CTkComboBox(select_date_time,width=90,values=mon,height=30)
    month.grid(row=1,column=1,padx=10,sticky='e',pady=20)
    ctk.CTkLabel(select_date_time,text="Date :",font=("Calibri",20)).grid(pady=20,row=1,column=2,sticky='w')
    Date=ctk.CTkComboBox(select_date_time,width=60,values=dt,height=30)
    Date.grid(row=1,column=3,pady=20,padx=10,sticky='e')
    ctk.CTkButton(select_date_time,text="Set Date & Time",font=("Calibri",13),
                    command=setdt).grid(pady=20,row=3,column=0,columnspan=4,padx=50,rowspan=2)
    
    win.wait_window(select_date_time)
    return [date,time]

def update_task(id,mode):
    all_tasks=[]
    with open("to_do_list_task.json","r") as f:
            all_tasks=json.load(f)

    if mode=="set_complete":
        for task in all_tasks:
            if task["id"]==id:
                task["completed"]=True
                for job in scheduler.get_jobs():
                    if job.id and (job.id == f'morning_{id}' or job.id == f'before_due_{id}'):
                        scheduler.remove_job(job.id)
                break
    if mode=="set_important":
        for task in all_tasks:
            if task["id"]==id:
                if task["section"]!="important":
                    task["is_important"]=True
                break
    if mode=="set_duedate":
        date_time=set_date()
        for task in all_tasks:
            if task["id"]==id:
                task["due_date"]=date_time[0]
                task["due_time"]=str(date_time[1])
                break
    with open("to_do_list_task.json","w") as f:
        json.dump(all_tasks,f,indent=4)
    load_task()

def delete_task(frame,task_id):
    all_tasks=[]
    with open("to_do_list_task.json","r") as f:
        all_tasks=json.load(f)
    
    for job in scheduler.get_jobs():
        if job.id and (job.id == f'morning_{task_id}' or job.id == f'before_due_{task_id}'):
            scheduler.remove_job(job.id)
            
    new_list=[]
    for task in all_tasks:
        if task["id"]!=task_id:
            new_list.append(task)
    frame.destroy()
    with open("to_do_list_task.json","w") as f:
        json.dump(new_list,f,indent=4)
        
    load_task()

def show_menu(event,frame,id,section):
    x_pos=event.x_root
    y_pos=event.y_root+25
    menu=tk.Menu(master=win,tearoff=0,bg="gray20",fg="white",activebackground="gray50",activeforeground="white")
    menu.add_command(label="Mark as Completed",command=lambda:update_task(id,"set_complete"))
    menu.add_command(label="Mark as Important",command=lambda:update_task(id,"set_important"))
    if section=="important":
        menu.add_command(label="Set Due Date",command=lambda:update_task(id,"set_duedate"))    
    menu.add_command(label="Delete Task",command=lambda:delete_task(frame,id))
    menu.post(x_pos,y_pos)

def load_task():
    # Clear all existing scheduler jobs to avoid duplicate notifications
    for job in scheduler.get_jobs():
        job.remove()
    for widget in tasks_today.winfo_children():
        widget.destroy()
    for widget in tasks_imp.winfo_children():
        widget.destroy()
    for widget in tasks_plan.winfo_children():
        widget.destroy()
    for widget in tasks_com.winfo_children():
        widget.destroy()
    for widget in tasks_uncom.winfo_children():
        widget.destroy()
    all_tasks=[]
    now_date=datetime.date.today()
    try:
        with open("to_do_list_task.json","r") as f:
            all_tasks=json.load(f)
    except:
        pass

    today_task,imp_task,plan_task,com_task,uncom_task,uniqu_task=[],[],[],[],[],[]
    for task in all_tasks:
        due_date=datetime.datetime.strptime(task["due_date"],"%m/%d/%y").date()
        # Notification ko load karte samay schedule karo
        if not task["completed"] and task["due_date"] != "None":
            date_str = task["due_date"]
            time_str = task["due_time"]
            try:
                due_datetime_obj = datetime.datetime.strptime(f"{date_str} {time_str}", "%m/%d/%y %H:%M")
            except ValueError:
                  due_datetime_obj = datetime.datetime.strptime(f"{date_str} {time_str}", "%m/%d/%y %H:%M:%S")
            if due_datetime_obj > datetime.datetime.now():
                
                morning_notification_time = due_datetime_obj.replace(hour=9, minute=0)
                if morning_notification_time > datetime.datetime.now():
                    scheduler.add_job(
                        show_notification,
                        'date',
                        run_date=morning_notification_time,
                        args=['To-Do List Reminder', f'Aaj aapka "{task["task_name"]}" task due hai.'],
                        id=f'morning_{task["id"]}'
                    )

                time_before_due = due_datetime_obj - datetime.timedelta(hours=1)
                if time_before_due > datetime.datetime.now():
                    scheduler.add_job(
                        show_notification,
                        'date',
                        run_date=time_before_due,
                        args=['To-Do List Reminder', f'1 ghante mein "{task["task_name"]}" task due hai.'],
                        id=f'before_due_{task["id"]}'
                    )
        if task["completed"]:
            com_task.append(task)
            continue
        if task["section"]=="today" and due_date==now_date:
            if task["is_important"]:
                uniqu_task.append(task)
            else:
                today_task.append(task)
        elif task["section"]=="important" and due_date>=now_date:
            imp_task.append(task)
        elif task["section"]=="planned" and due_date>=now_date:
            if task["is_important"]:
                uniqu_task.append(task)
            else:
                plan_task.append(task)
        else:
            uncom_task.append(task)

    for task in uniqu_task:
        due_date=datetime.datetime.strptime(task["due_date"],"%m/%d/%y").date()
        if due_date==now_date:
            task_frame=ctk.CTkFrame(tasks_today,border_color="purple",border_width=2,corner_radius=15,height=15)
            task_frame.pack(pady=5,fill="x")
            task_frame.pack_propagate(False)
            task_frame.grid_columnconfigure(0,weight=1)
            ctk.CTkLabel(task_frame,text=task["task_name"]+"  ("+task["due_date"]+")",font=("Arial",15),text_color="purple").grid(pady=2,padx=13,row=0,column=0,sticky='w')                    
            options=ctk.CTkButton(task_frame,text=":",height=5,width=15,font=("Arial",15))
            options.grid(row=0,column=1,sticky='e',padx=15)
            options.bind("<Button-1>",lambda event,id=task["id"],frame=task_frame:show_menu(event,frame,id,"uni"))
        if task["section"]=="planned":
            task_frame=ctk.CTkFrame(tasks_plan,border_color="purple",border_width=2,corner_radius=15,height=15)
            task_frame.pack(pady=5,fill="x")
            task_frame.pack_propagate(False)
            task_frame.grid_columnconfigure(0,weight=1)
            ctk.CTkLabel(task_frame,text=task["task_name"]+"  ("+task["due_date"]+")",font=("Arial",15),text_color="purple").grid(pady=2,padx=13,row=0,column=0,sticky='w')                    
            options=ctk.CTkButton(task_frame,text=":",height=5,width=15,font=("Arial",15))
            options.grid(row=0,column=1,sticky='e',padx=15)
            options.bind("<Button-1>",lambda event,id=task["id"],frame=task_frame:show_menu(event,frame,id,"uni"))

    
    for task in imp_task:
        due_date=datetime.datetime.strptime(task["due_date"],"%m/%d/%y").date()
        if due_date==now_date:
            task_frame=ctk.CTkFrame(tasks_today,border_color="red",border_width=2,corner_radius=15,height=15)
            task_frame.pack(pady=5,fill="x")
            task_frame.pack_propagate(False)
            task_frame.grid_columnconfigure(0,weight=1)
            ctk.CTkLabel(task_frame,text=task["task_name"],font=("Arial",15),text_color="red").grid(pady=2,padx=13,row=0,column=0,sticky='w')                    
            options=ctk.CTkButton(task_frame,text=":",height=5,width=15,font=("Arial",15))
            options.grid(row=0,column=1,sticky='e',padx=15)
            options.bind("<Button-1>",lambda event,id=task["id"],frame=task_frame:show_menu(event,frame,id,"today"))

        task_frame=ctk.CTkFrame(tasks_imp,border_color="gray60",border_width=2,corner_radius=15,height=15)
        task_frame.pack(pady=5,fill="x")
        task_frame.pack_propagate(False)
        task_frame.grid_columnconfigure(0,weight=1)
        ctk.CTkLabel(task_frame,text=task["task_name"]+"  ("+task["due_date"]+")",font=("Arial",15)).grid(pady=2,padx=13,row=0,column=0,sticky='w')                    
        options=ctk.CTkButton(task_frame,text=":",height=5,width=15,font=("Arial",15))
        options.grid(row=0,column=1,sticky='e',padx=15)
        options.bind("<Button-1>",lambda event,id=task["id"],frame=task_frame:show_menu(event,frame,id,"important"))
    
    for task in plan_task:
        due_date=datetime.datetime.strptime(task["due_date"],"%m/%d/%y").date()
        if due_date==now_date:
            task_frame=ctk.CTkFrame(tasks_today,border_color="green",border_width=2,corner_radius=15,height=15)
            task_frame.pack(pady=5,fill="x")
            task_frame.pack_propagate(False)
            task_frame.grid_columnconfigure(0,weight=1)
            ctk.CTkLabel(task_frame,text=task["task_name"]+"  ("+task["due_date"]+")",font=("Arial",15),text_color="green").grid(pady=2,padx=13,row=0,column=0,sticky='w')                    
            options=ctk.CTkButton(task_frame,text=":",height=5,width=15,font=("Arial",15))
            options.grid(row=0,column=1,sticky='e',padx=15)
            options.bind("<Button-1>",lambda event,id=task["id"],frame=task_frame:show_menu(event,frame,id,"today"))

        task_frame=ctk.CTkFrame(tasks_plan,border_color="gray60",border_width=2,corner_radius=15,height=15)
        task_frame.pack(pady=5,fill="x")
        task_frame.pack_propagate(False)
        task_frame.grid_columnconfigure(0,weight=1)
        ctk.CTkLabel(task_frame,text=task["task_name"]+"  ("+task["due_date"]+")",font=("Arial",15)).grid(pady=2,padx=13,row=0,column=0,sticky='w')                    
        options=ctk.CTkButton(task_frame,text=":",height=5,width=15,font=("Arial",15))
        options.grid(row=0,column=1,sticky='e',padx=15)
        options.bind("<Button-1>",lambda event,id=task["id"],frame=task_frame:show_menu(event,frame,id,"planned"))
    
    for task in today_task:
        task_frame=ctk.CTkFrame(tasks_today,border_color="gray60",border_width=2,corner_radius=15,height=15)
        task_frame.pack(pady=5,fill="x")
        task_frame.pack_propagate(False)
        task_frame.grid_columnconfigure(0,weight=1)
        ctk.CTkLabel(task_frame,text=task["task_name"],font=("Arial",15)).grid(pady=2,padx=13,row=0,column=0,sticky='w')                    
        options=ctk.CTkButton(task_frame,text=":",height=5,width=15,font=("Arial",15))
        options.grid(row=0,column=1,sticky='e',padx=15)
        options.bind("<Button-1>",lambda event,id=task["id"],frame=task_frame:show_menu(event,frame,id,"today"))
    
    for task_c in com_task:
        task_frame=ctk.CTkFrame(tasks_com,border_color="gray60",border_width=2,corner_radius=15,height=15)
        task_frame.pack(pady=5,fill="x")
        task_frame.pack_propagate(False)
        task_frame.grid_columnconfigure(0,weight=1)
        ctk.CTkLabel(task_frame,text=task_c["task_name"],font=("Arial",15)).grid(pady=2,padx=13,row=0,column=0,sticky='w')                    
        options=ctk.CTkButton(task_frame,text="Delete",height=5,width=15,font=("Arial",15),
                              command=lambda id=task_c["id"],frame=task_frame:delete_task(frame,id))
        options.grid(row=0,column=1,sticky='e',padx=15)

    for task_u in uncom_task:
        task_frame=ctk.CTkFrame(tasks_uncom,border_color="gray60",border_width=2,corner_radius=15,height=15)
        task_frame.pack(pady=5,fill="x")
        task_frame.pack_propagate(False)
        task_frame.grid_columnconfigure(0,weight=1)
        ctk.CTkLabel(task_frame,text=task_u["task_name"],font=("Arial",15)).grid(pady=2,padx=13,row=0,column=0,sticky='w')                    
        options=ctk.CTkButton(task_frame,text="Delete",height=5,width=15,font=("Arial",15),
                              command=lambda id=task_u["id"],frame=task_frame:delete_task(frame,id))
        options.grid(row=0,column=1,sticky='e',padx=15)

# Load_Task Function is complete 

def add_task(section,date,task):
    global today,entry
    all_task=[]
    if task=="":
        messagebox.showerror("Task Error","Please enter a task")
        return
    try:
        with open("to_do_list_task.json","r") as f:
            all_task=json.load(f)
    except:
        all_task=[]
    
    # due_date aur due_time ko string format mein initialize karo
    due_date = None
    due_time = "23:59" 
    
    if section=="today":
        due_date = today.strftime("%m/%d/%y")
    elif section=="planned":
        due_date = date[0]
        # date[1] ek datetime.time object hai, ise string mein convert karo
        due_time = date[1].strftime("%H:%M")
    elif section=="important":
        # Abhi ke liye, important task ki date/time today hi rakhte hain
        due_date = today.strftime("%m/%d/%y")
        due_time = "23:59"

    new_task={
        "id":str(uuid.uuid4()),
        "task_name":task,
        "completed":False,
        "is_important":False, 
        "due_date":str(due_date),
        "due_time":str(due_time),
        "creation_time":str(datetime.datetime.now().time()),
        "section":section
    }
    
    if section == "important":
        new_task["is_important"] = True
        
    # Notifications sirf tab schedule honge jab due_date aur due_time available ho
    if due_date and due_time != "None":
        due_datetime_obj = datetime.datetime.strptime(f"{due_date} {due_time}", "%m/%d/%y %H:%M")
        
        if due_datetime_obj > datetime.datetime.now():
            
            # 1. Due Date ko subah notification
            morning_notification_time = due_datetime_obj.replace(hour=9, minute=0)
            if morning_notification_time > datetime.datetime.now():
                scheduler.add_job(
                    show_notification,
                    'date',
                    run_date=morning_notification_time,
                    args=['To-Do List Reminder', f'Aaj aapka "{new_task["task_name"]}" task due hai.'],
                    id=f'morning_{new_task["id"]}'
                )
                
            # 2. Due Time se 1 ghanta pehle notification
            time_before_due = due_datetime_obj - datetime.timedelta(hours=1)
            if time_before_due > datetime.datetime.now():
                scheduler.add_job(
                    show_notification,
                    'date',
                    run_date=time_before_due,
                    args=['To-Do List Reminder', f'1 ghante mein "{new_task["task_name"]}" task due hai.'],
                    id=f'before_due_{new_task["id"]}'
                )

    all_task.insert(0,new_task)
    with open("to_do_list_task.json","w") as f:
        json.dump(all_task,f,indent=4, default=str)
    entry.delete(0,ctk.END)
    load_task()

def add_task_button(section):
    global entry,today
    def set_date1():
        global date_time
        date_time=set_date()
        btn.configure(state="normal")

    def done():
        frame.destroy()
        if section=="today":
            add1.grid(pady=5,row=4,column=0,columnspan=2)
        elif section=="planned":
            add2.grid(pady=5,row=4,column=0,columnspan=2)
        elif section=="important":
            add3.grid(pady=5,row=4,column=0,columnspan=2)
    
    if section !="planned":
        if section=="today":
            add1.grid_forget()
            frame=ctk.CTkFrame(today_sec,height=30,width=480,fg_color='gray20')
        else:
            add3.grid_forget()
            frame=ctk.CTkFrame(important_sec,height=30,width=480,fg_color='gray20')
        frame.grid(row=4,column=0,columnspan=2,padx=4,pady=4)
        frame.grid_propagate(False)
        entry=ctk.CTkEntry(frame,width=250,corner_radius=10,font=("Georgia",15),text_color='black'
                    ,fg_color='gray80',border_color='black')
        entry.grid(row=0,column=0)
        ctk.CTkButton(frame,width=35,corner_radius=10,font=("Arial",20),text="Add",command=lambda:add_task(section,None,entry.get())).grid(row=0,column=1,padx=5)
        ctk.CTkButton(frame,width=35,corner_radius=10,font=("Arial",20),text="Done",command=done).grid(row=0,column=2,padx=5)
    else:
        add2.grid_forget()
        frame=ctk.CTkFrame(planned_sec,height=30,width=480,fg_color='gray20')
        frame.grid(row=4,column=0,columnspan=2,padx=4,pady=4)
        frame.grid_propagate(False)
        entry=ctk.CTkEntry(frame,width=200,corner_radius=10,font=("Georgia",15),text_color='black'
                 ,fg_color='gray80',border_color='black')
        entry.grid(row=0,column=0)
        date=ctk.CTkButton(frame,width=35,corner_radius=10,font=("Arial",10),text="Set\nDate",command=set_date1)
        date.grid(row=0,column=1,padx=5)
        btn=ctk.CTkButton(frame,width=35,corner_radius=10,state="disabled",font=("Arial",20),text="Add",command=lambda:add_task(section,date_time,entry.get()))
        btn.grid(row=0,column=2,padx=5)
        ctk.CTkButton(frame,width=35,corner_radius=10,font=("Arial",20),text="Done",command=done).grid(row=0,column=3,padx=5)

win=ctk.CTk()

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    send_end_of_day_notification,
    'cron',
    hour=global_settings["end_of_day_time"].split(":")[0],
    minute=global_settings["end_of_day_time"].split(":")[1],
    id='end_of_day_job'
)
win.geometry("400x500")
win.title("Bhavesh Ka To-Do List App")
# Top Frame
top_frame=ctk.CTkFrame(win,fg_color="black",height=500)
top_frame.pack(fill="x",expand=True)

# Today Section
today_sec=ctk.CTkFrame(top_frame,border_color="gray80",border_width=1,height=500,width=400,corner_radius=10)
today_sec.grid(row=0,column=0)
today_sec.grid_propagate(False)
today_sec.grid_columnconfigure(0, weight=1)
today_sec.grid_columnconfigure(1, weight=0)
today_sec.grid_rowconfigure(0, weight=0)
today_sec.grid_rowconfigure(1, weight=0)
today_sec.grid_rowconfigure(2, weight=0)
today_sec.grid_rowconfigure(3, weight=1)
today_sec.grid_rowconfigure(4, weight=0)
ctk.CTkLabel(today_sec,text="Today Tasks",font=("Arial",20,"bold"),text_color="gray80").grid(row=0,column=0,pady=7,columnspan=2)
today=datetime.date.today()
ctk.CTkLabel(today_sec,text=today.strftime("%A"),
             font=("Segoe UI",30,"bold"),text_color="gray80").grid(row=1,column=0,sticky='w',pady=4,padx=7)
ctk.CTkLabel(today_sec,text=today.strftime("%B %d , %Y"),
             font=("Segoe UI",15,"bold"),text_color="gray80").grid(row=2,column=0,padx=7,sticky='w')
ctk.CTkButton(today_sec,text="...",height=25,width=35,font=("Arial",17,"bold")).grid(row=1,column=1,sticky='e',padx=7)
tasks_today=ctk.CTkScrollableFrame(today_sec,width=350,height=300,
                             fg_color="gray20",label_text="Tasks",label_font=("Segoe UI",19,"bold"),)
tasks_today.grid(row=3,column=0,columnspan=2,sticky='n',pady=5)
add1=ctk.CTkButton(today_sec,text="+",font=("Arial",20,"bold"),width=60,corner_radius=50,command=lambda : add_task_button("today"))
add1.grid(pady=5,row=4,column=0,columnspan=2)

# Planned Section
planned_sec=ctk.CTkFrame(top_frame,border_color="gray80",border_width=1,height=500,width=400,corner_radius=10)
planned_sec.grid(row=0,column=1,padx=8)
planned_sec.grid_propagate(False)
planned_sec.grid_columnconfigure(0,weight=1)
planned_sec.grid_columnconfigure(1,weight=0)
planned_sec.grid_rowconfigure(0,weight=0)
planned_sec.grid_rowconfigure(1,weight=1)
planned_sec.grid_rowconfigure(2,weight=0)
ctk.CTkLabel(planned_sec,text="Planned Tasks",font=("Arial",20,"bold"),text_color="gray80").grid(row=0,column=0,pady=7,columnspan=2)
ctk.CTkButton(planned_sec,text="...",height=25,width=35,font=("Arial",17,"bold")).grid(row=1,column=1,sticky='e',padx=7)
tasks_plan=ctk.CTkScrollableFrame(planned_sec,width=350,height=300,
                             fg_color="gray20",label_text="Tasks",label_font=("Segoe UI",19,"bold"),)
tasks_plan.grid(row=3,column=0,columnspan=2,sticky='n',pady=5)
add2=ctk.CTkButton(planned_sec,text="+",font=("Arial",20,"bold"),width=60,corner_radius=50,command=lambda : add_task_button("planned"))
add2.grid(pady=5,row=4,column=0,columnspan=2)

# Important Section
important_sec=ctk.CTkFrame(top_frame,border_color="gray80",border_width=1,height=500,width=400)
important_sec.grid(row=0,column=2)
important_sec.grid_propagate(False)
important_sec.grid_columnconfigure(0,weight=1)
important_sec.grid_columnconfigure(1,weight=0)
important_sec.grid_rowconfigure(0,weight=0)
important_sec.grid_rowconfigure(1,weight=1)
important_sec.grid_rowconfigure(2,weight=0)
ctk.CTkLabel(important_sec,text="Important Tasks",font=("Arial",20,"bold"),text_color="gray80").grid(row=0,column=0,pady=7,columnspan=2)
ctk.CTkButton(important_sec,text="...",height=25,width=35,font=("Arial",17,"bold")).grid(row=1,column=1,sticky='e',padx=7)
tasks_imp=ctk.CTkScrollableFrame(important_sec,width=350,height=300,
                             fg_color="gray20",label_text="Tasks",label_font=("Segoe UI",19,"bold"),)
tasks_imp.grid(row=3,column=0,columnspan=2,sticky='n',pady=5)
add3=ctk.CTkButton(important_sec,text="+",font=("Arial",20,"bold"),width=60,corner_radius=50,command=lambda : add_task_button("important"))
add3.grid(pady=5,row=4,column=0,columnspan=2)

# Fourth Frame
fourth_frame=ctk.CTkFrame(top_frame,border_color="gray80",border_width=1,height=500,width=140)
fourth_frame.grid(row=0,column=3,padx=5)
fourth_frame.grid_propagate(False)
ctk.CTkLabel(fourth_frame,text="The\nTo-Do List\nApp",font=("Segoe UI",20,"bold")).grid(row=0,column=0,pady=30,padx=20)
ctk.CTkLabel(fourth_frame,text="By\nBhavesh\nRajpurohit",font=("Segoe UI",20,"bold")).grid(row=1,column=0,padx=20,pady=30)
settings_button = ctk.CTkButton(fourth_frame, text="Settings", command=settings_menu)
settings_button.grid(row=2, column=0, padx=5, pady=10)
# Bottom Frame
bottom_frame=ctk.CTkFrame(win,fg_color="black",height=180)
bottom_frame.pack(fill="x",expand=True)

# Completed Section
completed_section=ctk.CTkFrame(bottom_frame,border_color="gray80",border_width=1,height=180,width=680,corner_radius=10)
completed_section.grid(row=0,column=0)
completed_section.grid_propagate(False)
completed_section.grid_columnconfigure(0,weight=1)
completed_section.grid_rowconfigure(1,weight=1)
ctk.CTkLabel(completed_section,text="Completed Tasks : ",font=("Arial",20,"bold"),text_color="gray80").grid(row=0,column=0,pady=7,columnspan=2)
tasks_com=ctk.CTkScrollableFrame(completed_section,width=650,height=20,
                             fg_color="gray20",label_text="Tasks",label_font=("Segoe UI",19,"bold"),)
tasks_com.grid(row=1,column=0,columnspan=2,sticky='n',pady=5)

# UnCompleted Section
uncompleted_section=ctk.CTkFrame(bottom_frame,border_color="gray80",border_width=1,height=180,width=680,corner_radius=10)
uncompleted_section.grid(row=0,column=1)
uncompleted_section.grid_propagate(False)
uncompleted_section.grid_columnconfigure(0,weight=1)
uncompleted_section.grid_rowconfigure(1,weight=1)
ctk.CTkLabel(uncompleted_section,text="Uncompleted Tasks : ",font=("Arial",20,"bold"),text_color="gray80").grid(row=0,column=0,pady=7,columnspan=2)
tasks_uncom=ctk.CTkScrollableFrame(uncompleted_section,width=650,height=20,
                             fg_color="gray20",label_text="Tasks",label_font=("Segoe UI",19,"bold"),)
tasks_uncom.grid(row=1,column=0,columnspan=2,sticky='n',pady=5)

load_task()
win.mainloop()