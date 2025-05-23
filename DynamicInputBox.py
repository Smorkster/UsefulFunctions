from tkinter import Tk, Button, Entry, Label, N, S, E, W

class dynamic_inputbox():
    def __init__( self, title = "", message = "", input = False, input_show = None, preset_text = None, buttons = [ 'OK' ], default_button = None ):
        """
        Creates a dynamic message-/inputbox where you can specify message, if there should be any input and what buttons to display.
        Returns a tuple with entered input and which button was clicked.

        * title - Title of the inputbox window
        * message - Message to be displayed
        * input - Should an textbox be displayed to enable text input, default: False
        * input_show - A character to be displayed for characters entered in the textbox. Only applicable when input is True
        * preset_text - A text that will be shown in the textbox before input is given from user
        * buttons - A string list for buttons to be generated. Text of clicked button will be returned from inputbox
        * default_button - Which button should be the default returned value. This button will be focused from start, unless an textbox is displayed
        """

        self._inputtext = ""
        self._clicked_button = default_button
        self._default_button_to_focus = None
        self._master = Tk()
        self._master.title( title )
        self._master.bind( "<Escape>", lambda event: self.cancel() )
        self._master.resizable( False, False )
        self.e = None

        self.title = title
        self.message = message
        self.input = input
        self.input_show = input_show
        self.buttons = buttons
        self.default_button = default_button
        self.preset_text = preset_text

        self.show()

    def cancel( self ):
        self._inputtext = 'Cancel'
        self._clicked_button = ''
        self._master.destroy()

    def on_closing( self, button = None ):
        if self.e:
            self._inputtext = self.e.get()
        if button is not None:
            self._clicked_button = button
        self._master.destroy()

    def preset_keypress( self, event ):
        if self.e.get() == self.preset_text:
            self.e.delete( 0, 'end' )
            self.e.config( show = self.input_show[0] )

    def show( self ):
        for i in range( 3 ):
            self._master.rowconfigure( i, weight = 1 )
        for i in range( len( self.buttons ) ):
            self._master.columnconfigure( i, weight = 1 )

        if self.message:
            m = Label( self._master, text = self.message, justify = 'left' )
            m.grid( row = 0, column = 0, columnspan = len( self.buttons ), padx = 10, pady = 5, sticky = ( N, W ) )

        button_widgets = {}
        for i, btn_text in enumerate( self.buttons ):
            b = Button( self._master, text = btn_text, width = 10,
                       command = lambda t = btn_text: self.on_closing( t ),
                       font = ( 'Calibri', 12, 'bold' if btn_text == self.default_button else 'normal' ) )
            b.bind( "<Return>", lambda event, t = btn_text: self.on_closing( t ) )
            b.grid( row = 2, column = i, padx = 5, pady = 10 )
            button_widgets[ btn_text ] = b
            if btn_text == self.default_button or ( self.default_button is None and i == 0 ):
                self._default_button_to_focus = b

        if self.input:
            self.e = Entry( self._master )
            if self.input_show != None:
                # Using index to ensure only one character is used
                if self.preset_text == None:
                    self.e = Entry( self._master, show = self.input_show[0] )

            if self.preset_text:
                self.e.insert( 0, self.preset_text )
                self.e.bind( "<KeyPress>", self.preset_keypress )

            self.e.bind( "<Return>", lambda event: self.on_closing() )
            self.e.grid( row = 1, column = 0, columnspan = len( self.buttons ), padx = 10, pady = 5, sticky = ( N, S, E, W ) )
            self.e.focus_set()
        else:
            self.e = None

        self._master.update_idletasks()
        width = self._master.winfo_width()
        frm_width = self._master.winfo_rootx() - self._master.winfo_x()
        win_width = width + 2 * frm_width
        height = self._master.winfo_height()
        titlebar_height = self._master.winfo_rooty() - self._master.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = self._master.winfo_screenwidth() // 2 - win_width // 2
        y = self._master.winfo_screenheight() // 2 - win_height // 2
        self._master.geometry(f'{ width }x{ height }+{ x }+{ y }')
        self._master.update_idletasks()

        self._master.attributes( '-topmost', True )
        self._master.protocol( "WM_DELETE_WINDOW", self.on_closing )

        self._master.focus_force()
        if self.input:
            self.e.focus()
        else:
            self._default_button_to_focus.focus()

        self._master.mainloop()

    def get( self ):
        return tuple( ( self._inputtext, self._clicked_button ) )

"""
if __name__ == '__main__':
    result = dynamic_inputbox("Test", "Enter password:", input=True, input_show='*', buttons=['Yes', 'No'], default_button='Yes', preset_text='YourPassword')
    r = result.get()
    breakpoint()
    print(tuple(result))
"""