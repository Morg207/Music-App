import tkinter as tk
import sys
import pygame
import os
from PIL import ImageTk, Image
from tkinter import filedialog

pygame.mixer.init()

state = {"music_dir": "",
         "selected_index": 0,"music_paused":False,
         "toggle_mute":1,"track_volume":1.0}

def resize_image(image_path,new_dimensions):
    resized_image = Image.open(image_path)
    resized_image = resized_image.resize(new_dimensions,Image.BILINEAR)
    resized_image = ImageTk.PhotoImage(resized_image)
    return resized_image

def load_songs():
    initial_directory = os.path.join(os.path.dirname(__file__),"..")
    abs_path = filedialog.askdirectory(title="Select Songs",initialdir=initial_directory,mustexist=True)
    if abs_path:
        state["music_dir"] = abs_path
        control_buttons["play"].config(state=tk.NORMAL)
        control_buttons["forward"].config(state=tk.NORMAL)
        control_buttons["backward"].config(state=tk.NORMAL)
        playlist.delete(0,tk.END)
        file_paths = os.listdir(state["music_dir"])
        for file_path in file_paths:
            desc = file_path[len(file_path)-4:]
            if desc != ".wav" and desc != ".mp3":
                continue
            playlist.insert(tk.END,file_path)
        playlist.select_set(0)
        first_item = playlist.get(0)
        state["selected_index"] = 0
        track_name.config(text=first_item)
        try:
            pygame.mixer.music.load(os.path.join(state["music_dir"],first_item))
        except:
            track_name.config(text="Song title...")
            pygame.mixer.music.unload()

def on_track_select(event):
    selection = playlist.curselection()
    if selection:
        state["music_paused"] = False
        playlist_index = selection[0]
        if state["selected_index"] != playlist_index:
            control_buttons["play"].config(state=tk.NORMAL)
            control_buttons["pause"].config(state=tk.DISABLED)
            control_buttons["stop"].config(state=tk.DISABLED)
            playlist_selection = playlist.get(playlist_index)
            track_name.config(text=playlist_selection)
            pygame.mixer.music.unload()
            track_to_load = os.path.join(state["music_dir"],playlist_selection)
            pygame.mixer.music.load(track_to_load)
            state["selected_index"] = playlist_index

def on_play():
    control_buttons["play"].config(state=tk.DISABLED)
    control_buttons["pause"].config(state=tk.NORMAL)
    control_buttons["stop"].config(state=tk.NORMAL)
    if not state["music_paused"]:
        try:
           pygame.mixer.music.play()
        except:
           play_button.config(state=tk.NORMAL)
           pause_button.config(state=tk.DISABLED)
    else:
        pygame.mixer.music.unpause()
        state["music_paused"] = False

def on_stop():
    control_buttons["play"].config(state=tk.NORMAL)
    control_buttons["pause"].config(state=tk.DISABLED)
    control_buttons["stop"].config(state=tk.DISABLED)
    pygame.mixer.music.stop()

def on_pause():
    control_buttons["play"].config(state=tk.NORMAL)
    control_buttons["stop"].config(state=tk.DISABLED)
    control_buttons["pause"].config(state=tk.DISABLED)
    pygame.mixer.music.pause()
    state["music_paused"] = True

def load_track():
    control_buttons["play"].config(state=tk.NORMAL)
    control_buttons["pause"].config(state=tk.DISABLED)
    playlist_selection = playlist.get(state["selected_index"])
    track_name.config(text=playlist_selection)
    pygame.mixer.music.unload()
    track_to_load = os.path.join(state["music_dir"],playlist_selection)
    pygame.mixer.music.load(track_to_load)

def on_backward():
    try:
        state["music_paused"] = False
        playlist.selection_clear(state["selected_index"])
        control_buttons["stop"].config(state=tk.DISABLED)
        state["selected_index"] -= 1
        if state["selected_index"] < 0:
            state["selected_index"] = 0
        playlist.select_set(state["selected_index"])
        load_track()
    except:
        pass

def on_forward():
    try:
        state["music_paused"] = False
        playlist.selection_clear(state["selected_index"])
        control_buttons["stop"].config(state=tk.DISABLED)
        state["selected_index"] += 1
        max_track_num = playlist.size()-1
        if state["selected_index"] > max_track_num:
            state["selected_index"] = max_track_num
        playlist.select_set(state["selected_index"])
        load_track()
    except:
        pass

def on_mute():
    state["toggle_mute"] *= -1
    if state["toggle_mute"] == -1:
        control_buttons["mute"].config(image=mute_on_image)
        pygame.mixer.music.set_volume(0.0)
    else:
        control_buttons["mute"].config(image=mute_off_image)
        pygame.mixer.music.set_volume(state["track_volume"])

def on_volume_changed(scale_value):
    current_volume = float(scale_value) / 10.0
    state["track_volume"] = current_volume
    pygame.mixer.music.set_volume(state["track_volume"])

def gen_playlist():
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
    return playlist_scrollbar, playlist_scrollbar_hor, playlist

def gen_volume_slider():
    volume_slider = tk.Scale(right_frame,from_=0,to=10,orient=tk.HORIZONTAL,cursor="hand2",font=("arial",11),length=110,command=on_volume_changed)
    volume_slider.set(10)
    volume_slider.pack(pady=(5,10))
    right_frame.pack(side=tk.LEFT,expand=True,fill="both",padx=(0,20),pady=(55,15))
    return volume_slider

def gen_track_details():
    welcome_message_frame = tk.Frame(left_frame,pady=20)
    welcome_message = tk.Label(welcome_message_frame,text="Welcome to EasyMusic!",fg="white",padx=3,pady=5,bg="green",relief=tk.RAISED)
    welcome_message.pack()
    welcome_message_frame.pack()
    music_image = resize_image("images/music notes.jpg",(400,300))
    music_image_label = tk.Label(left_frame,image=music_image,pady=20,relief=tk.RAISED,borderwidth=3)
    music_image_label.image = music_image
    music_image_label.pack()
    track_details_frame = tk.Frame(left_frame,pady=20)
    track_name = tk.Label(track_details_frame,text="Song title...",padx=20,font=("arial",10),wraplength=300,justify=tk.CENTER)
    track_name.pack(side=tk.LEFT)
    return track_details_frame, track_name

def create_icon_button(parent, image_path, command=None, state=tk.NORMAL):
    img = resize_image(image_path, (30, 30))
    btn = tk.Button(parent, image=img, bg="green", cursor="hand2", command=command, state=state)
    btn.image = img 
    btn.pack(side=tk.LEFT)
    return btn

def setup_controls(frame):
    button_data = [
        ("images/play.png", on_play),
        ("images/stop.png", on_stop),
        ("images/pause.png", on_pause),
        ("images/rewind.png", on_backward),
        ("images/fast forward.png", on_forward),
    ]
    buttons = []
    for path, cmd in button_data:
        btn = create_icon_button(frame, path, cmd, state=tk.DISABLED)
        buttons.append(btn)

    mute_btn = create_icon_button(frame,"images/mute off.png",on_mute)
    buttons.append(mute_btn)
    button_types = ("play","stop","pause","backward","forward")
    control_buttons = {}
    for i in range(len(button_types)):
        button_type = button_types[i]
        button = buttons[i]
        control_buttons[button_type] = button
    control_buttons["mute"] = buttons[5]
    return control_buttons

def close_app():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    window = tk.Tk()
    window.title("EasyMusic!")
    window.iconphoto(False, tk.PhotoImage(file="images/music app icon.png"))
    mute_off_image = resize_image("images/mute off.png", (30,30))
    mute_on_image = resize_image("images/mute on.png",(30,30))
    left_frame = tk.Frame(window)
    left_frame.pack(side=tk.LEFT, padx=(40, 20))

    track_details_frame, track_name = gen_track_details()
    load_songs_button = tk.Button(track_details_frame, text="Load songs", relief=tk.RAISED, fg="white", bg="green", cursor="hand2", command=load_songs)
    load_songs_button.pack(side=tk.LEFT)
    track_details_frame.pack()

    music_icon_frame = tk.Frame(left_frame)
    music_icon_frame.pack(pady=(0, 15))
    control_buttons = setup_controls(music_icon_frame)

    right_frame_label = tk.Label(text="Track playlist", font=25)
    right_frame = tk.LabelFrame(window, labelwidget=right_frame_label, borderwidth=5)
    playlist_scrollbar, playlist_scrollbar_hor, playlist = gen_playlist()
    volume_slider = gen_volume_slider()
    window.resizable(False,False)
    window.mainloop()
    close_app()
