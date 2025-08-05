import tkinter as tk

class AlwaysOnTopToolTip:
    """ A tooltip that appears when hovering over a widget, remains on top, and can be styled """
    def __init__( self, widget, msg, delay = 500, bg = "#ffffe0", font = ( "Calibri", 10 ), wraplength = 300 ):
        """ Initialize the tooltip with the widget, message, delay, background color, font, and wrap length """
        self.widget = widget
        self.text = msg
        self.delay = delay
        self.bg = bg
        self.font = font
        self.wraplength = wraplength
        self.tooltip_window = None
        self.after_id = None

        self.widget.bind( "<Enter>", self.schedule )
        self.widget.bind( "<Leave>", self.hide )
        self.widget.bind( "<Motion>", self.move )

    def schedule( self, event = None ):
        """ Schedule the tooltip to show after a delay """
        self.unschedule()
        self.after_id = self.widget.after( self.delay, self.show )

    def unschedule( self ):
        """ Cancel the scheduled tooltip display if it exists """
        if self.after_id:
            self.widget.after_cancel( self.after_id )
            self.after_id = None

    def move( self, event ):
        """ Move the tooltip to follow the mouse cursor """
        if self.tooltip_window:
            x, y = event.x_root + 20, event.y_root + 10
            self.tooltip_window.geometry( f"+{ x }+{ y }" )

    def show( self ):
        """ Show the tooltip at the current mouse position """
        if self.tooltip_window or not self.text:
            return

        x = self.widget.winfo_pointerx() + 20
        y = self.widget.winfo_pointery() + 10

        self.tooltip_window = tw = tk.Toplevel( self.widget )
        tw.wm_overrideredirect( True )
        tw.attributes( "-topmost", True )
        tw.geometry( f"+{ x }+{ y }" )

        label = tk.Label(
            tw,
            text = self.text,
            background = self.bg,
            borderwidth = 1,
            font = self.font,
            justify = 'left',
            padx = 5,
            pady = 5,
            relief = "solid",
            wraplength = self.wraplength
        )
        label.pack()

    def hide( self, event = None ):
        """ Hide the tooltip and clean up """
        self.unschedule()
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
