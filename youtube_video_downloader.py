import customtkinter as ctk
from pytubefix import YouTube,Search
import subprocess,os,requests,threading
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO
from tkinter import messagebox

class Download_process():
    def __init__(self,url=None):
        self.url=url
        if url:
            self.yt=YouTube(url,on_progress_callback=self.progress_callback)
    
    def progress_callback(self,stream,chunk,bytes_remaining):
        filesize=self.stream.filesize
        bytes_downloaded=filesize-bytes_remaining
        progress=bytes_downloaded/filesize
        win.after(0,self.update_progress_bar,progress)
    
    def update_progress_bar(self,progress):
        self.progress_bar.set(progress)
        size_mb=round(self.stream.filesize*progress/(1024*1024),2)
        self.txt.configure(text=f"{size_mb} MB")
            
    def start_download(self,stream):
        self.setup_gui()
        thread = threading.Thread(target=self.download_video, args=(stream,))
        thread.start()

    def setup_gui(self):
        for i in right_frame.winfo_children():
            i.destroy()
        
        ctk.CTkLabel(right_frame, text="Downloading....", font=("Arial",20)).pack(pady=10)
        self.progress_bar = ctk.CTkProgressBar(master=right_frame, orientation="horizontal", mode="determinate")
        self.progress_bar.set(0)
        self.progress_bar.pack(padx=10)
        self.txt = ctk.CTkLabel(right_frame, text="0.0 MB", font=("Arial", 10))
        self.txt.pack()

    def download_video(self,stream):
        self.stream=stream
        try:
            if stream.type=="video":
                self.max_audio=self.yt.streams.filter(abr="160kbps")
                self.stream.download(filename="Video.mp4")
                self.max_audio[0].download(filename="Audio.mp4")
                output_file=self.stream.title
                for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|', "'"]:
                    output_file=output_file.replace(char,"")
                output_file+=".mp4"
                video_file="Video.mp4"
                audio_file="Audio.mp4"
                command = [
                "ffmpeg",
                "-i", video_file,
                "-i", audio_file,
                "-c:v", "copy",
                "-c:a", "copy",
                output_file
            ]
                try:
                    win.after(0,self.merge_txt())
                    subprocess.run(command, check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    messagebox.showerror("Something is wrong","There is an issue on converting the video....")
                finally:
                    os.remove(video_file)
                    os.remove(audio_file)
            else:
                stream.download()
            win.after(0,self.update_gui)
        except Exception as e:
            self.txt.configure(text="Downloading fail...")

    def merge_txt(self):
        self.txt.configure(text="Merging....")

    def update_gui(self):
        self.txt.configure(text="Download complete")
        for widget in right_frame.winfo_children():
            widget.destroy()
        
        win.after(0,self.download_video_detials)

    def download_video_detials(self):
        resolutio,audio_track={},{}
        for i in self.yt.streams.filter(adaptive=True,type="video"):
            if i.resolution not in resolutio:
                resolutio[i.resolution]=i
            
        for i in self.yt.streams.filter(adaptive=True,type="audio"):
            if i.abr not in audio_track:
                audio_track[i.abr]=i

        ctk.CTkLabel(right_frame,text="Video Files",font=("Arial",13,"bold"),text_color="gray80").pack()
    
        for i,stream in resolutio.items():
            size=round(stream.filesize/(1024*1024),2)
            frame1=ctk.CTkFrame(right_frame,corner_radius=60,width=200,height=70,border_color="gray20",border_width=2)
            frame1.pack(pady=5)
            frame1.pack_propagate(False)
            ctk.CTkLabel(frame1,text=f"Quality : {i}  Size : {size}",font=("Arial",13)).pack(padx=10,pady=10)
            ctk.CTkButton(frame1,text="Download",height=20,width=30,font=("Arial",10),corner_radius=60,
                          command=lambda stre=stream:self.start_download(stre)).pack(padx=20)

        ctk.CTkLabel(right_frame,text="Audio Files",font=("Arial",13,"bold"),text_color="gray80").pack()

        for i,stream in audio_track.items():
            size=round(stream.filesize/(1024*1024),2)
            frame1=ctk.CTkFrame(right_frame,corner_radius=60,width=200,height=70,border_color="gray20",border_width=2)
            frame1.pack(pady=5)
            frame1.pack_propagate(False)
            ctk.CTkLabel(frame1,text=f"Quality : {i}  Size : {size}",font=("Arial",13)).pack(anchor='sw',padx=10,pady=10)
            ctk.CTkButton(frame1,text="Download",height=20,width=30,font=("Arial",10),corner_radius=60
                          ,command=lambda stre=stream:self.start_download(stre)).pack(padx=20)

class Process():
    def is_url(self,url):
        try:
            result=urlparse(url)
            return all([result.scheme,result.netloc])
        except:
            return False

    def search_process(self,url):
        for widget in loaded_video.winfo_children():
            widget.destroy()
        try:
            sr=Search(url)
            r=0
            for i in sr.videos:
                self.start_link_process(i.watch_url,r)
                r+=1
        except:
            messagebox.showerror("Something is wrong","There is a problem... Maybe not able to connect with internet.")

    def start_link_process(self,url,r=None):
            thread= threading.Thread(target=self.link_process, args=(url,r))
            thread.start()


    def link_process(self,url,r=None):
        try:
            if isinstance(url,str):
                yt=YouTube(url)
                title=yt.title
                length=yt.length
                likes=yt.likes
                img_data=requests.get(yt.thumbnail_url).content
            else:
                yt=url
                title=yt.title
                length=yt.length
                likes=yt.likes
                img_data=requests.get(yt.thumbnail_url).content
            win.after(0,self.update_gui,url,r,title,likes,length,yt,img_data)
        except:
            messagebox.showerror("Something is wrong","Please enetr correct url...")

    def update_gui(self,url,r,title,likes,length,yt,img_data):
        self.url=url
        
        frame=ctk.CTkFrame(loaded_video,height=250,width=550,border_color="gray20",border_width=5)
        frame.grid(row=r,column=0,pady=5)
        frame.grid_propagate(False)

        thumbnail_frame=ctk.CTkFrame(frame,height=250,width=350)
        thumbnail_frame.grid(row=0,column=0)
        thumbnail_frame.grid_propagate(False)
        
        img=Image.open(BytesIO(img_data))
        img=img.resize((350,250), Image.LANCZOS)
        ctk_image =ctk.CTkImage(light_image=img, dark_image=img, size=(350, 250))
        thumbnail_img=ctk.CTkLabel(thumbnail_frame,image=ctk_image,text="")
        thumbnail_img.grid(row=0,column=0)

        video_details=ctk.CTkFrame(frame,height=250,width=200)
        video_details.grid(row=0,column=1)
        video_details.grid_propagate(False)

        d1=Download_process(url)

        ctk.CTkLabel(video_details,text=f"  Video title : {title}",font=("Arial",15,"bold"),wraplength=195,anchor='nw').grid(row=0,column=0,sticky='w')
        ctk.CTkLabel(video_details,text=f"  Video length : {length}",font=("Arial",15,"bold"),wraplength=195).grid(row=1,column=0,sticky='w',pady=10)
        ctk.CTkLabel(video_details,text=f"  Total likes : {likes}",font=("Arial",15,"bold"),wraplength=195).grid(row=2,column=0,sticky='w')
        ctk.CTkButton(video_details,text="Download",font=("Arial",15),width=50,corner_radius=60,command= d1.download_video_detials).grid(row=3,column=0,sticky='w')

    def check(self,url):
        for widget in loaded_video.winfo_children():
            widget.destroy()
        if self.is_url(url):
                self.start_link_process(url)
        else:
            self.search_process(url)

p1=Process()
win=ctk.CTk()
win.geometry("800x600")
win.title("YouTube Video Downloader")

frame_top=ctk.CTkFrame(win,height=200,width=700,border_color="gray60",border_width=3)
frame_top.pack()
frame_top.pack_propagate(False)
ctk.CTkLabel(frame_top,text="YouTube Video Downloader by   B_R_P",font=("Arial",30)).pack(pady=10)
ctk.CTkLabel(frame_top,text="You can download by pasting the video link or by search about video in search bar"
             ,font=("Arial",15),anchor='nw').pack(pady=20)
search_bar=ctk.CTkEntry(frame_top,placeholder_text="Enter video link or search video",border_color="gray60",width=600,corner_radius=60)
search_bar.pack()
load_btn=ctk.CTkButton(frame_top,text="Find Video",width=100,corner_radius=20,command=lambda : p1.check(search_bar.get()))
load_btn.pack(pady=10)

bottom_frame=ctk.CTkFrame(win,height=10,width=10)
bottom_frame.pack(expand=True,fill="both",pady=10)
bottom_frame.pack_propagate(False)
loaded_video=ctk.CTkScrollableFrame(bottom_frame,height=360,width=550,border_width=2,border_color="gray40")
loaded_video.grid(row=0,column=0)
right_frame=ctk.CTkScrollableFrame(bottom_frame,height=360,width=195,border_color="gray40",border_width=2)
right_frame.grid(row=0,column=1,padx=5)
win.mainloop()