from tkinter import Tk, Button, Entry, Label, N, S, E, W

def dynamic_inputbox(title="", message="", input=True, input_show = None, buttons=['OK'], default_button=None):
    inputtext = ""
    clicked_button = default_button
    master = Tk()
    master.title(title)
    master.bind( "<Escape>", lambda event: cancel() )
    master.resizable(False, False)

    for i in range(3):
        master.rowconfigure(i, weight=1)
    for i in range(len(buttons)):
        master.columnconfigure(i, weight=1)

    if message:
        m = Label(master, text=message)
        m.grid(row=0, column=0, columnspan=len(buttons), padx=10, pady=5, sticky=W)

    def cancel():
        nonlocal inputtext, clicked_button
        inputtext = 'Cancel'
        clicked_button = ''
        master.destroy()

    def on_closing(button=None):
        nonlocal inputtext, clicked_button
        if e:
            inputtext = e.get()
        if button != None:
            clicked_button = button
        master.destroy()

    button_widgets = {}
    for i, btn_text in enumerate(buttons):
        if btn_text == default_button:
            b = Button(master, text=btn_text, width=10, command=lambda t=btn_text: on_closing(t), font = ( 'Calibri', 12, 'bold' ) )
        else:
            b = Button(master, text=btn_text, width=10, command=lambda t=btn_text: on_closing(t), font = ( 'Calibri', 12 ) )
        b.bind( "<Return>", lambda event: on_closing( btn_text ) )
        b.grid(row=2, column=i, padx=5, pady=10)
        button_widgets[btn_text] = b

    # Focus the default button if provided (or the first one)
    if default_button in button_widgets:
        button_widgets[default_button].focus_set()

    if input:
        if input_show == None:
            e = Entry( master )
        else:
            e = Entry(master, show=input_show)
        e.bind( "<Return>", lambda event: on_closing() )
        e.grid(row=1, column=0, columnspan=len(buttons), padx=10, pady=5, sticky = ( N, S, E, W ) )
        e.focus_set()
    else:
        e = None

    master.update_idletasks()
    width = master.winfo_width()
    frm_width = master.winfo_rootx() - master.winfo_x()
    win_width = width + 2 * frm_width
    height = master.winfo_height()
    titlebar_height = master.winfo_rooty() - master.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = master.winfo_screenwidth() // 2 - win_width // 2
    y = master.winfo_screenheight() // 2 - win_height // 2
    master.geometry( f'{ width }x{ height }+{ x }+{ y }')

    master.protocol("WM_DELETE_WINDOW", on_closing)
    master.mainloop()

    return inputtext, clicked_button
