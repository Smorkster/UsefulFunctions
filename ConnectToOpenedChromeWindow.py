from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_cd_path():
    dummy_options = ChromeOptions()
    dummy_options.add_argument( '--headless' )
    dummy = webdriver.Chrome( options = dummy_options )
    p = dummy.service.path
    dummy.quit()
    return webdriver.Chrome( options = dummy_options ).service.path

#if ChromeDriverManager().driver.get_browser_version_from_os() != ChromeDriverManager().driver.get_driver_version_to_download():
#    print( "Uppdaterar Chrome driver" )
#    ChromeDriverManager().install()

#print( ChromeDriverManager().driver.get_browser_version_from_os() )
#print( ChromeDriverManager().driver.get_driver_version_to_download() )
breakpoint()
options = ChromeOptions()
options.debugger_address = "127.0.0.1:" + '123412341234'
browser = webdriver.Chrome( service = Service( executable_path = get_cd_path() ), options = options )
#browser = webdriver.Chrome( options = options )

#browser.find_element( By.XPATH, f"//div[ @class = 'sc_variable_editor' and contains( ., 'Efternamn, mellannamn (enligt Skatteverket)' ) ]//input[1]" ).get_attribute( 'value' )
browser.get( "https://contoso.com/u/0/#in?compose=new" )
breakpoint()
browser.quit()
#browser.find_element( By.ID, "img-highlight-uid40c3" )
