"""
Create a tooltip widget that will stay on top

* widget - The Tk widget the tooltip is associated with.
* msg - The text to place in the tooltip.
* delay - Time, in milliseconds, to wait before the tooltip is shown. Default is 10.
"""
import tkinter as tk

class AlwaysOnTopToolTip:
    def __init__( self, widget, msg, delay = 10 ):
        self.widget = widget
        self.text = msg
        self.delay = delay
        self.tooltip_window = None
        self.after_id = None

        self.widget.bind( "<Enter>", self.schedule )
        self.widget.bind( "<Leave>", self.hide )
        self.widget.bind( "<Motion>", self.move )

    def schedule( self, event = None ):
        self.after_id = self.widget.after( self.delay, self.show )

    def move( self, event ):
        if self.tooltip_window:
            x, y = event.x_root + 20, event.y_root + 10
            self.tooltip_window.geometry( f"+{ x }+{ y }" )

    def show( self ):
        if self.tooltip_window or not self.text:
            return

        x, y = self.widget.winfo_pointerx() + 20, self.widget.winfo_pointery() + 10
        self.tooltip_window = tw = tk.Toplevel( self.widget )
        tw.wm_overrideredirect( True )
        tw.attributes( "-topmost", True )  # Critical for top stacking
        tw.geometry( f"+{ x }+{ y }" )

        label = tk.Label(
            master = tw,
            background = "#ffffe0",
            borderwidth = 1 ,
            font = ( 'Calibri', 10 ),
            justify = 'left',
            padx = 5,
            pady = 5,
            relief = "solid",
            text = self.text,
            wraplength = 300
            )
        label.pack()
        label.update_idletasks()

        x = self.widget.winfo_pointerx() + 20
        y = self.widget.winfo_pointery() + 10
        tw.geometry( f"+{ x }+{ y }" )

    def hide( self, event = None ):
        if self.after_id:
            self.widget.after_cancel( self.after_id )
            self.after_id = None

        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

