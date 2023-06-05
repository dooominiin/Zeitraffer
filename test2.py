def select_string(bool_array):
    selected_frames = [str(i) for i, is_frame_bright in enumerate(bool_array) if is_frame_bright]  # Liste der Indexe, bei denen der Wert True ist
    ffmpeg_select_string = "+".join([f"eq(n,{frame_index})" for frame_index in selected_frames])  # Erstelle den String im gewünschten Format
    return f"select='{ffmpeg_select_string}',setpts=N/FRAME_RATE/TB"



is_bright = [False, True, True, False, True, True, True, False]  # Beispiel-Array mit booleschen Werten
string = select_string(is_bright)
print(string)  # Ausgabe des erstellten Strings