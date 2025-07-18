from tkinter import Frame, Radiobutton, StringVar, Tk, Button, Entry, Label, N, S, E, W
from tkinter.font import Font
from typing import Dict, List, Optional, Union

class dynamic_inputbox():
    def __init__( self,
                 title = "",
                 message = "",
                 input = False,
                 input_default = '',
                 input_show = None,
                 preset_text = None,
                 # Label, Default, Show, Preset
                 inputs: Optional[ List[ Dict[ str, Union[ str, None ] ] ] ] = None,
                 alternatives: Optional[ List[ Dict[ str, Union[ str, List[ str ] ] ] ] ] = None,
                 buttons: Optional[ List[ str ] ] = [ 'OK' ],
                 default_button: Optional[str] = None
                ):
        """
        A dynamic and customizable input dialog box using Tkinter.

        This class creates a GUI dialog that can display a message, 
        accept one or more text inputs (with optional presets, default values, 
        and masked input), offer grouped radio button alternatives, and allow 
        the user to respond via custom buttons.

        Parameters:
            title (str): The window title. Default is an empty string.
            message (str): An optional message to be displayed above inputs.
            input (bool): If True, a single text input field is displayed using input_default, input_show, and preset_text.
                        If False, 'inputs' must be used to specify fields. Default is False.
            input_default (str): Default value for the single input field (used only if 'input' is True).
            input_show (Optional[str]): Character used to mask input (e.g., '*') for the single input field.
            preset_text (Optional[str]): Greyed-out preset text for the single input field, replaced on key press.
            inputs (Optional[List[Dict[str, Union[str, None]]]]): A list of input definitions. Each input is a dict with optional keys:
                - 'label': Display label for the input field (required).
                - 'default': Pre-filled value.
                - 'show': Character to display instead of actual input (e.g., '*').
                - 'preset': Greyed-out prompt text, removed on typing.
            alternatives (Optional[List[Dict[str, Union[str, List[str]]]]]): A list of grouped radio button sets. Each group is a dict with:
                - 'label': Group name (required).
                - 'options': List of option strings (required).
                - 'default': Pre-selected option (defaults to the first in 'options').
            buttons (Optional[List[str]]): A list of button labels to display. The clicked button is returned. Default is ['OK'].
            default_button (Optional[str]): Which button should be pre-focused. If not set, the first button is focused (unless inputs exist).

        Returns:
            The class itself does not return a value upon instantiation. 
            To access the user's input after the dialog closes, use the `get()` method.

            - `get(dictionary=False)` returns a tuple:
                (inputs_dict, alternatives_dict, clicked_button)
                - inputs_dict: a dictionary mapping each input's label to the entered value.
                - alternatives_dict: a dictionary mapping each alternative group to the selected option.
                - clicked_button: the label of the button clicked by the user.

            - `get(dictionary=True)` returns a single dictionary:
                {
                    'inputs': {...},         # as above
                    'alternatives': {...},   # as above
                    'button': '...'          # clicked button label
                }
        """

        self._inputtext = ""
        self._clicked_button = default_button
        self._default_button_to_focus = None
        self._master = Tk()
        self._master.title( title )
        self._master.bind( "<Escape>", lambda event: self.cancel() )
        self._master.resizable( False, False )
        self.input_fields = {}
        self.alternatives_vars = {}
        self.e = None

        self.title = title
        self.message = message

        self.input = input
        self.input_show = input_show
        self.preset_text = preset_text
        self.input_default = input_default

        if input and not inputs:
            self.inputs = [ { 'label': 'Input', 'default': input_default, 'show': input_show, 'preset': preset_text } ]
        else:
            self.inputs = inputs

        self.alternatives = alternatives

        self.buttons = buttons
        self.default_button = default_button

        self.show()

    def cancel( self ):
        self._inputtext = 'Cancel'
        self._clicked_button = ''
        self._master.destroy()

    def on_closing( self, button = None ):
        self._inputtext = {
            'inputs': [ ( label, field.get() ) for label, field in self.input_fields.items() ],
            'alternatives': [ ( label, var.get() ) for label, var in self.alternatives_vars.items() ]
        }

        if button is not None:
            self._clicked_button = button

        self._master.destroy()

    def preset_keypress( self, event ):
        input_item = next( ( item for item in self.inputs if item.get( 'label' ) == 'Test 4' ), None )
        if event.widget.get() == input_item.get( 'preset' ) and Font( font = event.widget.cget( 'font' ) ).actual().get( 'slant' ) == 'italic':
            event.widget.delete( 0, 'end' )
        event.widget.config( font = ( 'Calibri', 12, 'normal' ), show = input_item.get( 'show' ), fg = '#000000' )

    def show( self ):
        row_index = 0

        # Setup columns for each button
        for i in range( len( self.buttons ) ):
            self._master.columnconfigure( i, weight = 1 )

        if self.message:
            m = Label( self._master, text = self.message, justify = 'left' )
            m.grid( row = 0, column = 0, columnspan = len( self.buttons ), padx = 10, pady = 5, sticky = ( N, W ) )
            row_index = 1

        if self.inputs:
            for i, input in enumerate( self.inputs ):
                label_text = input.get( 'label', f'Field { i }' )
                default = input.get( 'default', '' )
                show = input.get( 'show', None )
                preset = input.get( 'preset', None )

                lbl = Label( self._master, text = label_text )
                lbl.grid( row = row_index + i, sticky = W, padx = 10 )

                entry = Entry( self._master, font = ( 'Calibri', 12, 'normal' ) )
                entry.winfo_name()
                entry.insert( 0, default )
                entry.grid( row = row_index + i + 1, padx = 10, pady = 2, sticky = ( W, E ) )
                self.input_fields[label_text] = entry

                # show = show[0] if show else None , 
                if preset:
                    if not default:
                        entry.insert( 0, preset )
                        entry.config( foreground = '#D3D3D3' , font = ( 'Calibri', 12, 'italic' ) )
                else:
                    if show:
                        entry.config( show = show[0] if show else None )

                entry.bind( "<KeyPress>", self.preset_keypress )
                row_index += 1

        row_index += len( self.inputs )
        if self.alternatives:
            for j, alternative in enumerate( self.alternatives ):
                grp_frame = Frame( master = self._master )
                grp_frame.grid( row = row_index + j, column = 0, sticky = W )
                label = alternative.get( 'label', f'Group { j }' )
                options = alternative.get( 'options', [] )
                default = alternative.get( 'default', options[0] if options else '' )
                var = StringVar( value = default )
                self.alternatives_vars[label] = var

                Label( master = grp_frame, text = label , font = ( 'Calibri', 14, 'bold' ) ).grid( columnspan = len( options ) )

                for i, option in enumerate( options ):
                    rb = Radiobutton( grp_frame, text = option, variable = var, value = option )
                    rb.grid( row = row_index + j, column = 1 + i, sticky = W, padx = 5 )

        row_index += 1
        for i, btn_text in enumerate( self.buttons ):
            b = Button( master = self._master, text = btn_text, width = 10,
                       command = lambda t = btn_text: self.on_closing( t ),
                       font = ( 'Calibri', 12, 'bold' if btn_text == self.default_button else 'normal' ) )
            b.bind( "<Return>", lambda event, t = btn_text: self.on_closing( t ) )
            b.grid( row = row_index, column = i, padx = 5, pady = 10 )
            if btn_text == self.default_button or ( self.default_button is None and i == 0 ):
                self._default_button_to_focus = b

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

    def get( self, dictionary = False ):
        if not dictionary:
            return ( self._inputtext[ 'inputs' ], self._inputtext[ 'alternatives' ], self._clicked_button )
        else:
            return {
                'inputs': dict( self._inputtext[ 'inputs' ] ),
                'alternatives': dict( self._inputtext[ 'alternatives' ] ),
                'button': self._clicked_button
            }

""" Example usage
if __name__ == '__main__':
    result = dynamic_inputbox(
        title = 'test',
        message = 'test msg',
        buttons = ['ok','cans'],
        default_button = 'ok',
        inputs = [
            { 'label':'Test 1' },
            { 'label':'Test 2', 'default': 'Test default' },
            { 'label':'Test 3', 'show': '*' },
            { 'label':'Test 4', 'preset': 'test preset' , 'show':'p'}
            ],
        alternatives = [
            {'label': 'Role', 'options': ['Admin', 'User'], 'default': 'User'}
            ],
        )
    r = result.get()
    rr = result.get( dictionary = True )
    print( r )
"""