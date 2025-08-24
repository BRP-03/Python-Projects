from pytubefix import YouTube

yt=YouTube("https://youtu.be/2_ufYaJNi7w?si=wI2D0nHw12C0Sjpi")
stream=yt.streams.get_highest_resolution()
stream.download()
print("Downloaded")