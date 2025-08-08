""" This is an example of how to use the dynamic_inputbox class."""

from dynamicinputbox import dynamic_inputbox

tests = dynamic_inputbox(
        title = 'test',
        message = 'test msg',
        buttons = ['ok','cans'],
        default_button = 'ok',
        inputs = [
            { 'label':'Test 1' },
            { 'label':'Test 2', 'name': 'T2', 'default': 'Test default' },
            { 'label':'Test 3', 'show': '*' },
            { 'label':'Test 4', 'preset': 'test preset' , 'show': 'p' }
            ],
        alternatives = [
            {'label': 'Role', 'options': ['Admin', 'User'], 'default': 'User'},
            {'label': 'Role 2', 'options': ['Admin 2', 'User 2'], 'default': 'User'}
            ],
        group_separator = True
    )
r = tests.get()
print( r )
rr = tests.get( dictionary = True , wipe_after_get = True )
#print( rr )
try:
    print( list( rr[ 'inputs' ] ) )
except:
    pass

dlg = dynamic_inputbox(
    title = "Login",
    message = "Enter your credentials",
    inputs = [
        { 'label': 'Username' , 'name': 'Username' },
        { 'label': 'Password', 'show': '*' }
    ],
    buttons = [ 'OK', 'Cancel' ]
)

# First retrieval — password returned as plain string, SecureString wiped
result1 = dlg.get( dictionary = False, wipe_after_get = True )
try:
    #print( 'First call:', result1['inputs']['Username'] )
    print( f'First call: { result1 }' )
    print( 'First call password:', result1['inputs']['Password'] )
except:
    pass

# Second retrieval — password is now gone
result2 = dlg.get( dictionary = True, wipe_after_get = True )
try:
    print( 'Second call:', result2['inputs']['Username'] )
    print( 'Second call password:', result2['inputs']['Password'] )
except:
    pass
print( 'done' )