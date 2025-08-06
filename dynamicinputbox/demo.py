""" This is an example of how to use the dynamic_inputbox class."""

from dynamicinputbox import dynamic_inputbox

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
        {'label': 'Role', 'options': ['Admin', 'User'], 'default': 'User'},
        {'label': 'Role 2', 'options': ['Admin 2', 'User 2'], 'default': 'User'}
        ],
    )
r = result.get()
print( r )
rr = result.get( dictionary = True )
print( rr )
print( list( rr.get( 'inputs' , {} ).values() )[0] )
