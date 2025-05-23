import re
import os
import subprocess
import threading

from tkinter import *
from tkinter import ttk
from tktooltip import ToolTip

class ScriptInfo:
    def __init__( self, filename ):
        self.filename = filename
    
    def add_attr( self, attr_name, attr_val ):
        setattr( self, attr_name, attr_val )

def extract_scriptinfo( file ):
    si = ScriptInfo( file )
    with open( file[2], encoding='utf-8' ) as f:
        lines = f.read()

    regex_script_info_block = r"ScriptInfo\s*(.*?)\s*ScriptInfoEnd"
    block_match = re.search( regex_script_info_block, lines, re.DOTALL )

    for p, t in re.findall( r"#\s*(\w+)\s*-\s*(.+)" , block_match.group( 1 ) ):
        si.add_attr( p, t )

    return si

def click_handler():
    msg = " "
    tt = " "
    def set_text():
        nonlocal msg
        global active_run_info
        active_run_info.config( text = msg )

    def set_tt():
        nonlocal tt
        return tt

    script_path = active_file[2].replace( '\\\\', '\\' )

    def run_script():
        nonlocal msg
        nonlocal tt
        msg = "Väntar ..."
        tt = ""
        set_text()

        try:
            result = subprocess.run( [ 'python', script_path ], capture_output = True, text = True , start_new_session = True )
            if result.returncode == 0:
                msg = f"Done"
            else:
                msg = f"Error occured, see tooltip"
                tt = result.stderr
        except Exception as e:
            msg = f"Error occured, see tooltip"
            tt = str( e )
        set_text()

    # Run script in a background thread
    run_script()

def init_click_handler( file, script_run_info ):
    global submit_thread
    global active_file
    global active_run_info
    active_file = file
    active_run_info = script_run_info

    submit_thread = threading.Thread( target = click_handler )
    submit_thread.daemon = True
    submit_thread.start()
    #root.after(20, check_submit_thread)

def create_script_controls( main_frame, script_info, name, enumerated_file ):
    script_name_label = ttk.Label( main_frame, text = name )
    script_name_label.grid( column = 0 , row = enumerated_file[0] , sticky = ( W ) )
    ToolTip( script_name_label, msg = script_info.Description )

    script_run_button = ttk.Button( main_frame, text = "Run" , command = lambda:init_click_handler( enumerated_file, script_run_info ) )
    script_run_button.grid( column = 1 , row = enumerated_file[0] )

    script_run_info = ttk.Label( main_frame, text = "" , width = 100 )
    script_run_info.grid( column = 2 , row = enumerated_file[0] , sticky = ( N, S, E, W ) )
    ToolTip( script_run_info, msg = "" )

root = Tk()
content = ttk.Frame( root, padding = ( 5, 5, 5, 5 ) )
content.grid( column = 0, row = 0, sticky = ( N, S, E, W ) )
content.grid( sticky = ( N, S, E, W ) )

folder = '../RunFiles'
#breakpoint()
directory = os.path.join( os.path.dirname( os.path.dirname( __file__ ) ), "RunFiles" )
indexed_files = [ ( i, f, os.path.join( directory, f ) ) for i, f in enumerate(
    sorted(
        [ f for f in os.listdir( directory ) if os.path.isfile( os.path.join( directory, f ) ) ],
        key = lambda x: x.lower()
    )
) ]

for file in indexed_files:
    if file[1].endswith( ".py" ):
        scriptinfo = extract_scriptinfo( file )
        name_base = os.path.splitext( file[1] )[0]
        create_script_controls( content, scriptinfo, name_base, file )
        content.columnconfigure( 0, weight = 0 )
        content.columnconfigure( 1, weight = 0 )
        content.columnconfigure( 2, weight = 3 )
        content.rowconfigure( file[0], weight = 0 )

root.columnconfigure(0, weight = 1 )
root.rowconfigure(0, weight = 0 )
root.mainloop()
