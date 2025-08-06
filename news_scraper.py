import requests,tkinter as tk,threading
from bs4 import BeautifulSoup
from tkinter import ttk,messagebox,Toplevel,filedialog
from itertools import zip_longest   

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36"
}
#This function will scrap all the titles in Hindustan newspaper , all headlines and the link to read articles.
def HT():
    titles.delete(0,tk.END)
    url="https://www.hindustantimes.com/"
    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.content,"html.parser")
    title=soup.find_all("span",class_="hdgStyle")
    titles.insert(tk.END," Top News")
    global a_ht
    a_ht={" Top News":0}
    j=1
    for i in title:
        try:
            txt=" "
            txt+=i.find("a").text
            a_ht[txt]=j
            titles.insert(tk.END,txt)
        except :
            None
        j+=1
    global divs_ht,ht_article
    ht_article={}
    divs_ht=soup.find_all("div",class_="htImpressionTracking")
    for i in divs_ht:
        h2=i.find_all("h2")
        for j in h2:
            tag=j.find("a")
            link=tag.get("href")
            ht_article[tag.text]=link

#This function is used to scrap all headlines of Indian Express of pre-defined titles and the link to read articles.
def IE():
    titles.delete(0,tk.END)
    global ie_top_new,ie_latest,ie_lifestyle,ie_business,ie_world,ie_technology,ie_sport,ie_trending,ie_education
    ie_top_new,ie_latest,ie_business,ie_sport,ie_trending,ie_education,ie_lifestyle,ie_world,ie_technology={},{},{},{},{},{},{},{},{}
    lis=["Top News","Latest News","Lifestyle","Business News","World News","Technology","Sports","Trending","Education"]
    for i in lis:
        titles.insert(tk.END,i)
    url="https://www.indianexpress.com/"
    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.content,"html.parser")
    div_left_sidebar=soup.find("div",class_="left-sidebar")
    top_div=div_left_sidebar.find_all("div",class_="content-txt")
    latest_div=div_left_sidebar.find_all("ul")[1].find_all("li")
    for i,j in zip(top_div,latest_div):
        ie_top_new[i.find("a").text]=i.find("a").get("href")
        ie_latest[j.find("a").text]=j.find("a").get("href") 
    business_div=div_left_sidebar.find("div",id="HP_BUSINESS").find("div",class_="left-panel").find_all("a")+div_left_sidebar.find("div",id="HP_BUSINESS").find("div",class_="right-panel").find_all("a")
    sport_div=div_left_sidebar.find("div",id="HP_SPORTS").find("div",class_="left-panel").find_all("a")+div_left_sidebar.find("div",id="HP_SPORTS").find("div",class_="right-panel").find_all("a")
    for i,j in zip_longest(sport_div,business_div,fillvalue=None):
        try: ie_sport[i.text]=i.get("href")
        except: None
        try: ie_business[j.text]=j.get("href")
        except: None
    trend_div=div_left_sidebar.find("div",id="HP_TRENDING").find("div",class_="business-right").find_all("a")+div_left_sidebar.find("div",id="HP_TRENDING").find("div",class_="business-left").find_all("a")
    edu_div=div_left_sidebar.find("div",id="HP_EDUCATION").find("div",class_="business-left").find_all("a")+div_left_sidebar.find("div",id="HP_EDUCATION").find("div",class_="business-right").find_all("a")
    techno_div=div_left_sidebar.find("div",id="HP_TECHNOLOGY").find("div",class_="business-left").find("h4").find_all("a")+div_left_sidebar.find("div",id="HP_TECHNOLOGY").find("div",class_="business-right").find_all("a")
    for i,j,k in zip(edu_div,trend_div,techno_div):
        ie_education[i.text]=i.get("href")
        ie_trending[j.text]=j.get("href")
        ie_technology[k.text]=k.get("href")
    div_right_sidebar=soup.find("div",class_="right-sidebar")
    div_x=div_right_sidebar.find("div",class_="usual")
    life_div=div_x.find_next("div").find_all("div",class_="heading")
    world_div=div_right_sidebar.find("div",id="HP_WORLD").find_all("div",class_="heading")
    for i,j in zip_longest(life_div,world_div,fillvalue=None):
        try:
            ie_world[j.find("a").text]=j.find("a").get("href")
        except:
            pass
        ie_lifestyle[i.find("a").text]=i.find("a").get("href")

def DB():
    titles.delete(0,tk.END)
    url="https://www.bhaskarenglish.in/"
    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.content,"html.parser")
    ul=soup.find_all("ul",limit=5)
    global data
    data={}
    divs=ul[4].find_all("div",recursive=False)
    key="Top News"
    values=[]
    for i in divs:
        try:
            h3=i.find("h3")
            link=h3.find_previous("a").get("href")
            values.append({h3.text:link})
        except:
            data[key]=values
            values=[]
            span=i.find("span").find_next("div").text
            titles.insert(tk.END,key)
            key=span          

#This function is used to show headlines of selected newspapers's selected title.    
def show_headlines_part(e):
    global divs_ht,a_ht,selected_paper,ht_article,data
    global ie_top_new,ie_latest,ie_lifestyle,ie_business,ie_world,ie_technology,ie_sport,ie_trending,ie_education
    
#This is used to show all healines for selected title of Hindustan Times paper.
    if selected_paper=="Hindustan Times":
        if not titles.curselection():
            return
        for item in tree.get_children():
            tree.delete(item)
        a=titles.get(titles.curselection())
        b=a_ht[a]
        local_div=divs_ht[b]
        h2=local_div.find_all("h2")
        for i in h2:
            tex=i.find('a').text
            tree.insert("", "end", values=(tex,))
            tree.insert("", "end", values=("",)) 

#This is used to show all healines for selected title of The Indian Express paper.
    if selected_paper=="The Indian Express":
        if not titles.curselection():
            return
        for item in tree.get_children():
            tree.delete(item)
        a=titles.get(titles.curselection())
        dict={}
        if a=="Top News":
            dict=ie_top_new
        elif a=="Latest News":
            dict=ie_latest
        elif a=="Lifestyle":
            dict=ie_lifestyle
        elif a=="World News":
            dict=ie_world
        elif a=="Business News":
            dict=ie_business
        elif a=="Technology":
            dict=ie_technology
        elif a=="Sports":
            dict=ie_sport
        elif a=="Trending":
            dict=ie_trending
        elif a=="Education":
            dict=ie_education
        for i in dict:
            if not i:
                continue
            tree.insert("", "end", values=(i,))
            tree.insert("", "end", values=("",)) 
    elif selected_paper=="Dainik Bhaskar":
        if not titles.curselection():
            return
        for item in tree.get_children():
            tree.delete(item)
        global ab
        ab=titles.get(titles.curselection())
        for i in data[ab]:
            for j in i:
                tree.insert("", "end", values=(j,))
                tree.insert("", "end", values=("",)) 

#This function is used for insert article of selected headline in another tab.
def see_article(e):
    global ht_article,data,ab
    global ie_top_new,ie_latest,ie_lifestyle,ie_business,ie_world,ie_technology,ie_sport,ie_trending,ie_education
    note.select(frame_b) 
    article.config(state="normal")
    selected = tree.focus()
    if selected:
        values=tree.item(selected,'values')
        if values==('',):
            tree.selection_remove(selected)
    if not selected:
        return  
    values = tree.item(selected)['values']
    if not values:
        return
    heading = values[0]

#This is used to get article of Heading of Hindustan times.
    if selected_paper=="Hindustan Times":
        if heading in ht_article:
            article.delete(1.0,tk.END)
            url=ht_article[heading]
            response=requests.get(url,headers=headers)
            soup=BeautifulSoup(response.content,"html.parser")
            divs=soup.find("div",class_="storyDetails taboola-readmore")
            content="\t"
            try:
                paras=divs.find_all("p")
                article.delete("1.0",tk.END) 
                for i in paras:
                    content+=i.text
                    content+="\n\t"
                article.insert("1.0",content)
            except :
                article.insert("1.0","Sorry , but able to find the article.... :(")
        article.config(state="disabled")

#This is used to get article of Heading of The Indian Express.
    elif selected_paper=="The Indian Express":
        article.delete(1.0,tk.END)
        check={}
        if heading in ie_business:
            check=ie_business
        elif heading in ie_education:
            check=ie_education
        elif heading in ie_latest:
            check=ie_latest
        elif heading in ie_lifestyle:
            check=ie_lifestyle
        elif heading in ie_sport:
            check=ie_sport
        elif heading in ie_technology:
            check=ie_technology
        elif heading in ie_top_new:
            check=ie_top_new
        elif heading in ie_trending:
            check=ie_trending
        elif heading in ie_world:
            check=ie_world
        url=check[heading]
        response=requests.get(url,headers=headers)
        soup=BeautifulSoup(response.content,"html.parser")
        try:
            head=soup.find("h1").text+"\n"+soup.find("h2").text
            paras=soup.find_all("p")
            content=head+"\n"
            for i in paras:
                content+=i.text+"\n\t"
            article.insert(tk.END,content)
        except:
            article.insert(tk.END,"Sorry , not able to get article.\nMaybe its a network error or the article you want is only for subscribers.:(")
        article.config(state="disabled")
        
    elif selected_paper=="Dainik Bhaskar":
        article.delete(1.0,tk.END)
        for i in data[ab]:
            for j in i :
                if j==heading:
                    link="".join(i.values())
        url="https://www.bhaskarenglish.in/"+link
        response=requests.get(url)
        soup=BeautifulSoup(response.content,"html.parser")
        paras=soup.find("article").find_all("p")
        content="\t"
        for i in paras:
            content+=i.text+"\n\t"
        article.insert(tk.END,content)
        article.config(state="disabled")

def select(e):
    global selected_paper
    selected_paper=paper.get()
    for item in tree.get_children():
        tree.delete(item)
    article.delete(1.0,tk.END)
    def run_scraper():
        if selected_paper=="Hindustan Times":
            HT()
        elif selected_paper=="The Indian Express":
            IE()
        elif selected_paper=="Dainik Bhaskar":
            DB()
    threading.Thread(target=run_scraper).start()


def save():
    check=article.get(1.0,2.0).strip()
    if not check:
        messagebox.showerror("No Article","There is not article to save.")
        return
    content=article.get(1.0,tk.END)
    filepath=filedialog.asksaveasfilename(
        title="Save Article",
        filetypes=[("*.txt","Text File")]
    )
    with open (filepath,"w",encoding="utf-8") as f:
        f.write(content)
def style():
    top=tk.Toplevel(win)
    top.title("Article Formatting")
    top.geometry("300x200")
    tk.Label(top,text="Font Family : ",font=("Arial",11)).grid(row=1,column=1,sticky='w')
    font_list = ["Arial", "Calibri", "Cambria", "Comic Sans MS", "Courier New", "Georgia",
    "Helvetica", "Impact", "Lucida Console", "MS Sans Serif", "Segoe UI","Tahoma" ,
    "Times New Roman", "Trebuchet MS", "Verdana", "TkDefaultFont", "TkFixedFont",
    "TkMenuFont", "TkTextFont", "TkHeadingFont"]
    family=ttk.Combobox(top,values=font_list)
    family.grid(row=1,column=2)
    family.set("Arial")
    frame=tk.Frame(top,height=50,width=300)
    frame.grid(row=2,column=1,columnspan=2,pady=20)
    var=tk.StringVar()
    var.set("normal")
    tk.Radiobutton(frame,text="Normal",variable=var,value="normal",font=("Arial",11)).grid(row=1,column=1)
    tk.Radiobutton(frame,text="Bold",variable=var,value="bold",font=("Arial",11)).grid(row=1,column=2)
    tk.Radiobutton(frame,text="Itallic",variable=var,value="italic",font=("Arial",11)).grid(row=1,column=3)
    tk.Label(top,text="Font Size : ",font=("Arial",11)).grid(row=3,column=1,sticky='w')
    size=tk.StringVar()
    tk.Spinbox(top,from_=1,to=40,increment=1,textvariable=size).grid(row=3,column=2)
    size.set(13)
    def done():
        article.config(font=(family.get(),size.get(),var.get()),state="disabled")
        top.destroy()
    tk.Button(top,text="Save",font=("Arial",13),command=done,width=15).grid(row=4,column=1,pady=30,sticky='w')
#GUI Code

win=tk.Tk()
win.geometry("800x650")
theme=ttk.Style()
theme.theme_use("clam")
main_menu=tk.Menu(win)
win.config(menu=main_menu)
menus=tk.Menu(main_menu,tearoff=0)
main_menu.add_cascade(label="Menus",menu=menus)
menus.add_command(label="Save Article",command=save)
menus.add_command(label="Article Formatting",command=style)
menus.add_separator()
menus.add_command(label="Exit",command=win.destroy)
note=ttk.Notebook(win)
note.pack(expand=True,fill="both")
frame_a=tk.Frame(note)
frame1=tk.Frame(frame_a,bg="paleturquoise",height=150,width=800)
frame1.pack(fill="x")
frame1.pack_propagate(True)
paper=tk.StringVar()
news_paper=["Hindustan Times","The Indian Express","Dainik Bhaskar"]
tk.Label(frame1,text="Select news paper : ",bg="paleturquoise",font=("Arial",13)).grid(row=1,column=1,sticky='w')
papers=ttk.Combobox(frame1,values=news_paper,font=("Arial",13),textvariable=paper)
papers.grid(row=2,column=1,sticky='nw')
papers.bind("<<ComboboxSelected>>",select)
tk.Label(frame1,text="Titles : ",bg="paleturquoise",font=("Arial",13)).grid(padx=200,row=1,column=2,sticky='w')
titles=tk.Listbox(frame1,height=7,width=12,font=("Segoe UI",13,"bold"))
titles.grid(row=2,column=2,sticky='e',padx=200)
titles.bind("<<ListboxSelect>>",show_headlines_part)
tk.Label(frame1,text="",bg="paleturquoise",font=("arial",5)).grid(row=3,column=1)
frame2 = tk.Frame(frame_a, bg="lightpink", height=90, width=800)
frame2.pack(expand=True, fill="both")
tree_style=ttk.Style()
tree_style.configure("mystyle.Treeview",font=("Segoe UI",13))
tree_style.configure("mystyle.Treeview",font=("Segoe UI",13,"bold"))
columns=("Headline",)
tree = ttk.Treeview(frame2, columns=columns, show='headings', selectmode='browse',style="mystyle.Treeview")
tree.heading("Headline", text="Headline")
tree.column("Headline", width=500, anchor='w')
vsb = ttk.Scrollbar(frame2, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
tree.grid(row=0, column=0, sticky="nsew")
vsb.grid(row=0, column=1, sticky='ns')
frame2.grid_rowconfigure(0, weight=1)
frame2.grid_columnconfigure(0, weight=1)
tree.bind("<<TreeviewSelect>>", see_article)
note.add(frame_a,text="NewsPaper & Headings")
frame_b=tk.Frame(note)
article=tk.Text(frame_b,wrap="word",height=10,width=10,font=("Arial",13),state="disabled")
article.pack(expand=True,fill="both")
note.add(frame_b,text="Article")
win.mainloop()