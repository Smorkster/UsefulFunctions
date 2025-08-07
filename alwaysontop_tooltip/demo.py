import tkinter as tk
from alwaysontop_tooltip import AlwaysOnTopToolTip

def main():
    root = tk.Tk()
    root.title( "AlwaysOnTopToolTip Demo" )
    root.geometry( "300x200" )

    label = tk.Label( root, text = "Hover over me", font = ( "Arial", 14 ) )
    label.pack( pady = 50 )

    AlwaysOnTopToolTip(
        label,
        msg = "This is an always-on-top tooltip, with blinking effect, that appears when you hover over Tkinter widgets.",
        delay = 500,
        bg = "#f0f0f0",
        font = ( "Verdana", 10 ),
        wraplength = 350,
        borderstyle = 'solid',
        borderwidth = 2,
        stationary = True,
        blink={
            "enabled": True,
            "interval": 200,
            "mode": "opacity",
            "min_alpha": -2.3,
            "max_alpha": 1.0,
            "step": 0.9,
            "duration": 3000  # Stops after 3 seconds
        }
        )

    root.mainloop()

if __name__ == "__main__":
    main()
