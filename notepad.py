from tkinter import *
from tkinter import ttk, filedialog, messagebox

root = Tk()

# Define functions for menu commands
def new_file():
    text.delete(1.0, END)

def open_file():
    file = filedialog.askopenfile(mode='r', filetypes=[('Text Files', '*.txt')])
    if file:
        content = file.read()
        text.delete(1.0, END)
        text.insert(INSERT, content)

def save_file():
    file = filedialog.asksaveasfile(defaultextension='.txt', filetypes=[('Text Files', '*.txt')])
    if file:
        file.write(text.get(1.0, END))
        file.close()

def exit_notepad():
    root.quit()

def cut_text():
    text.event_generate("<<Cut>>")

def copy_text():
    text.event_generate("<<Copy>>")

def paste_text():
    text.event_generate("<<Paste>>")

# Font size tracking for zoom
current_font_size = 12  # Set initial font size
current_font = "Arial"  # Default font

def zoomin_text():
    global current_font_size
    current_font_size += 2
    text.config(font=(current_font, current_font_size))

def zoomout_text():
    global current_font_size
    current_font_size -= 2
    if current_font_size >= 6:  # Prevent font size going too small
        text.config(font=(current_font, current_font_size))

def about_notepad():
    messagebox.showinfo("About", "Notepad by Yuvansh😎")

# Font changing functionality
def change_font():
    selected_font = font_listbox.get(ACTIVE)
    global current_font
    current_font = selected_font
    text.config(font=(current_font, current_font_size))

def change_font_color():
    selected_color = fontcolor_listbox.get(ACTIVE)
    text.config(fg=selected_color)

def change_font_size():
    selected_size = fontsize_listbox.get(ACTIVE)
    global current_font_size
    current_font_size = int(selected_size)
    text.config(font=(current_font, current_font_size))

# Window configuration
root.title("Notepad")
root.geometry("800x600")
root.configure(background="black")

# Text Widget
text = Text(root, undo=True, wrap='word', font=(current_font, current_font_size))
text.pack(expand=True, fill=BOTH)

# Menu bar setup
menu = Menu(root)
root.config(menu=menu)

# File menu
filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='New', command=new_file, accelerator="Ctrl+N")
filemenu.add_command(label='Open...', command=open_file, accelerator="Ctrl+O")
filemenu.add_command(label='Save', command=save_file, accelerator="Ctrl+S")
filemenu.add_separator()
filemenu.add_command(label='Exit', command=exit_notepad, accelerator="Alt+F4")

# Edit menu
editmenu = Menu(menu, tearoff=0)
menu.add_cascade(label='Edit', menu=editmenu)
editmenu.add_command(label='Undo', command=lambda: text.edit_undo(), accelerator="Ctrl+Z")
editmenu.add_command(label='Redo', command=lambda: text.edit_redo(), accelerator="Ctrl+Y")
editmenu.add_separator()
editmenu.add_command(label='Cut', command=cut_text, accelerator="Ctrl+X")
editmenu.add_command(label='Copy', command=copy_text, accelerator="Ctrl+C")
editmenu.add_command(label='Paste', command=paste_text, accelerator="Ctrl+V")
editmenu.add_separator()
editmenu.add_command(label='Select All', command=lambda: text.tag_add(SEL, "1.0", END), accelerator="Ctrl+A")

# Format menu
formatmenu = Menu(menu, tearoff=0)
menu.add_cascade(label='Format', menu=formatmenu)
formatmenu.add_command(label='Word Wrap', command=lambda: None)  # Placeholder

# Font menu
fontmenu = Menu(formatmenu, tearoff=0)
formatmenu.add_cascade(label='Font Style', menu=fontmenu)
fontmenu.add_command(label='Change Font', command=lambda: font_selection_popup())
fontmenu.add_command(label='Font Color', command=lambda: font_color_selection_popup())
fontmenu.add_command(label='Font size', command=lambda: font_size_selection_popup())

# View menu
viewmenu = Menu(menu, tearoff=0)
menu.add_cascade(label='View', menu=viewmenu)
zoommenu = Menu(viewmenu, tearoff=0)
viewmenu.add_cascade(label='Zoom', menu=zoommenu)
zoommenu.add_command(label='Zoom In', command=zoomin_text, accelerator="Ctrl++")
zoommenu.add_command(label='Zoom Out', command=zoomout_text, accelerator="Ctrl+-")
zoommenu.add_command(label='Restore Default Zoom', command=lambda: text.config(font=(current_font, 12)))

viewmenu.add_command(label='Status Bar', command=lambda: None)  # Placeholder

# Help menu
helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='View Help', command=lambda: None)  # Placeholder for help
helpmenu.add_separator()
helpmenu.add_command(label='About Notepad', command=about_notepad)

# Scrollbar
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text.yview)

# Font selection popup
def font_selection_popup():
    top = Toplevel(root)
    top.title("Select Font")
    top.geometry("200x200")

    global font_listbox
    font_listbox = Listbox(top)
    fonts = ['Arial', 'Calibri', 'Cooper Black', 'Courier', 'Segoe Script', 'French Script MT', 'Times New Roman', 'Helvetica', 'Verdana']
    
    for font in fonts:
        font_listbox.insert(END, font)
    
    font_listbox.pack(fill=BOTH, expand=True)

    # Select button
    select_button = Button(top, text="Select", command=lambda: [change_font(), top.destroy()])
    select_button.pack(pady=10)

# Font color selection popup
def font_color_selection_popup():
    top = Toplevel(root)
    top.title("Select Font Color")
    top.geometry("200x200")

    global fontcolor_listbox
    fontcolor_listbox = Listbox(top)
    font_colors = ['red', 'blue', 'black', 'brown', 'green', 'yellow', 'violet', 'indigo']
    
    for color in font_colors:
        fontcolor_listbox.insert(END, color)
    
    fontcolor_listbox.pack(fill=BOTH, expand=True)

    # Select button
    select_button = Button(top, text="Select", command=lambda: [change_font_color(), top.destroy()])
    select_button.pack(pady=10)

# Font size selection popup
def font_size_selection_popup():
    top = Toplevel(root)
    top.title("Select Font Size")
    top.geometry("200x200")

    global fontsize_listbox
    fontsize_listbox = Listbox(top)
    font_sizes = [6, 8, 10, 12, 15, 20, 22, 25, 28, 35]
    
    for size in font_sizes:
        fontsize_listbox.insert(END, size)
    
    fontsize_listbox.pack(fill=BOTH, expand=True)

    # Select button
    select_button = Button(top, text="Select", command=lambda: [change_font_size(), top.destroy()])
    select_button.pack(pady=10)

# Bind shortcut keys
root.bind('<Control-n>', lambda event: new_file())
root.bind('<Control-o>', lambda event: open_file())
root.bind('<Control-s>', lambda event: save_file())
root.bind('<Control-x>', lambda event: cut_text())
root.bind('<Control-c>', lambda event: copy_text())
root.bind('<Control-v>', lambda event: paste_text())
root.bind('<Control-plus>', lambda event: zoomin_text())
root.bind('<Control-minus>', lambda event: zoomout_text())

# Main loop
root.mainloop()
