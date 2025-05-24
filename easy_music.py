import tkinter as tk
import pygame
import os
from PIL import ImageTk, Image
from tkinter import filedialog

pygame.mixer.init()

def resize_image(image_path,new_dimensions):
    resized_image = Image.open(image_path)
    resized_image = resized_image.resize(new_dimensions,Image.BILINEAR)
    resized_image = ImageTk.PhotoImage(resized_image)
    return resized_image

def load_songs():
    initial_directory = os.path.join(os.path.dirname(__file__),"..")
    local_path = filedialog.askdirectory(title="Select Songs",initialdir=initial_directory,mustexist=True)
    if local_path:
        global music_path
        music_path = local_path
        play_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.NORMAL)
        playlist.delete(0,tk.END)
        file_paths = os.listdir(music_path)
        for file_path in file_paths:
            desc = file_path[len(file_path)-4:]
            if desc != ".wav" and desc != ".mp3":
                continue
            playlist.insert(tk.END,file_path)
        playlist.select_set(0)
        first_item = playlist.get(0)
        global selected_index
        selected_index = 0
        track_name.config(text=first_item)
        try:
            pygame.mixer.music.load(os.path.join(music_path,first_item))
        except:
            track_name.config(text="Song title...")
            pygame.mixer.music.unload()

def on_track_select(event):
    selection = playlist.curselection()
    global selected_index
    if selection:
        playlist_index = selection[0]
        if selected_index != playlist_index:
            play_button.config(state=tk.NORMAL)
            stop_button.config(state=tk.NORMAL)
            pause_button.config(state=tk.DISABLED)
            playlist_selection = playlist.get(playlist_index)
            track_name.config(text=playlist_selection)
            pygame.mixer.music.unload()
            track_to_load = os.path.join(music_path,playlist_selection)
            pygame.mixer.music.load(track_to_load)
            selected_index = playlist_index

def on_play():
    play_button.config(state=tk.DISABLED)
    pause_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.NORMAL)
    global music_paused
    if not music_paused:
        try:
           pygame.mixer.music.play()
        except:
           play_button.config(state=tk.NORMAL)
           pause_button.config(state=tk.DISABLED)
    else:
        pygame.mixer.music.unpause()
        music_paused = False

def on_stop():
    play_button.config(state=tk.NORMAL)
    pause_button.config(state=tk.DISABLED)
    pygame.mixer.music.stop()

def on_pause():
    play_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    pygame.mixer.music.pause()
    global music_paused
    music_paused = True

def load_track():
    play_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.NORMAL)
    pause_button.config(state=tk.DISABLED)
    playlist_selection = playlist.get(selected_index)
    track_name.config(text=playlist_selection)
    pygame.mixer.music.unload()
    track_to_load = os.path.join(music_path,playlist_selection)
    pygame.mixer.music.load(track_to_load)

def on_back():
    try:
        global selected_index
        playlist.selection_clear(selected_index)
        selected_index -= 1
        if selected_index < 0:
            selected_index = 0
        playlist.select_set(selected_index)
        load_track()
    except:
        pass

def on_forward():
    try:
        global selected_index
        playlist.selection_clear(selected_index)
        selected_index += 1
        max_track_num = playlist.size()-1
        if selected_index > max_track_num:
            selected_index = max_track_num
        playlist.select_set(selected_index)
        load_track()
    except:
        pass

def on_mute():
    global toggle_state
    toggle_state *= -1
    if toggle_state == -1:
        mute_off_button.config(image=mute_on_button_image)
        pygame.mixer.music.set_volume(0.0)
    else:
        mute_off_button.config(image=mute_off_button_image)
        pygame.mixer.music.set_volume(track_volume)

def on_volume_changed(scale_value):
    global track_volume
    current_volume = float(scale_value) / 10.0
    track_volume = current_volume
    pygame.mixer.music.set_volume(current_volume)
    
if __name__ == "__main__":
    toggle_state = 1
    track_volume = 1
    music_paused = False
    window = tk.Tk()
    window.title("EasyMusic!")
    window.iconphoto(False,tk.PhotoImage(file="images/music app icon.png"))
    left_frame = tk.Frame(window)
    left_frame.pack(side=tk.LEFT,padx=(40,20))
    welcome_message_frame = tk.Frame(left_frame,pady=20)
    welcome_message = tk.Label(welcome_message_frame,text="Welcome to EasyMusic!",fg="white",padx=3,pady=5,bg="green",relief=tk.RAISED)
    welcome_message.pack()
    welcome_message_frame.pack()
    music_image = resize_image("images/music notes.jpg",(400,300))
    music_image_label = tk.Label(left_frame,image=music_image,pady=20,relief=tk.RAISED,borderwidth=3)
    music_image_label.pack()
    track_details_frame = tk.Frame(left_frame,pady=20)
    track_name = tk.Label(track_details_frame,text="Song title...",padx=20,font=("arial",10),wraplength=300,justify=tk.CENTER)

    track_name.pack(side=tk.LEFT)
    load_songs_button = tk.Button(track_details_frame,relief=tk.RAISED,fg="white",bg="green",text="Load songs",cursor="hand2",command=load_songs)
    load_songs_button.pack(side=tk.LEFT)
    track_details_frame.pack()
    music_icon_frame = tk.Frame(left_frame)
    play_button_image = resize_image("images/play.png",(30,30))
    play_button = tk.Button(music_icon_frame,image=play_button_image,bg="green",cursor="hand2",command=on_play,state=tk.DISABLED)
    play_button.pack(side=tk.LEFT)
    stop_button_image = resize_image("images/stop.png",(30,30))
    stop_button = tk.Button(music_icon_frame,image=stop_button_image,bg="green",cursor="hand2",command=on_stop,state=tk.DISABLED)
    stop_button.pack(side=tk.LEFT)
    pause_button_image = resize_image("images/pause.png",(30,30))
    pause_button = tk.Button(music_icon_frame,image=pause_button_image,bg="green",cursor="hand2",command=on_pause,state=tk.DISABLED)
    pause_button.pack(side=tk.LEFT)
    rewind_button_image = resize_image("images/rewind.png",(30,30))
    rewind_button = tk.Button(music_icon_frame,image=rewind_button_image,bg="green",cursor="hand2",command=on_back)

    rewind_button.pack(side=tk.LEFT)
    ff_button_image = resize_image("images/fast forward.png",(30,30))
    ff_button = tk.Button(music_icon_frame,image=ff_button_image,bg="green",cursor="hand2",command=on_forward)
    ff_button.pack(side=tk.LEFT)
    mute_off_button_image = resize_image("images/mute off.png",(30,30))
    mute_off_button = tk.Button(music_icon_frame,image=mute_off_button_image,bg="green",cursor="hand2",command=on_mute)
    mute_on_button_image = resize_image("images/mute on.png",(30,30))
    mute_off_button.pack(side=tk.LEFT)
    music_icon_frame.pack(pady=(0,15))
    right_frame_label = tk.Label(text="Track playlist",font=25)
    
    right_frame = tk.LabelFrame(window,labelwidget=right_frame_label,borderwidth=5)
    playlist_scrollbar = tk.Scrollbar(right_frame,orient=tk.VERTICAL,cursor="hand2")
    playlist_scrollbar_hor = tk.Scrollbar(right_frame,orient=tk.HORIZONTAL,cursor="hand2")
    playlist = tk.Listbox(right_frame,selectmode=tk.SINGLE,activestyle=tk.NONE,font=("arial",13),cursor="hand2",width=22,
                          xscrollcommand=playlist_scrollbar_hor.set,yscrollcommand=playlist_scrollbar.set)
    playlist_scrollbar.config(command=playlist.yview)
    playlist_scrollbar_hor.config(command=playlist.xview)
    playlist_scrollbar.pack(side=tk.RIGHT,fill="y")
    playlist.bind("<<ListboxSelect>>",on_track_select)
    playlist.pack(expand=True,fill="both")
    playlist_scrollbar_hor.pack(fill="x")
    volume_slider = tk.Scale(right_frame,from_=0,to=10,orient=tk.HORIZONTAL,cursor="hand2",font=("arial",11),length=110,command=on_volume_changed)
    volume_slider.set(10)
    volume_slider.pack(pady=(5,10))
    right_frame.pack(side=tk.LEFT,expand=True,fill="both",padx=(0,20),pady=(55,15))
    window.resizable(False,False)
    window.mainloop()
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
