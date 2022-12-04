import appscript
import time

def startCryptoBot():
    script_1 = "docker start freqtrade"
    appscript.app('Terminal').do_script(script_1)  # or any other command you choose

def startGUI():
    script_2 = "open -n -a 'Google Chrome' --args --new-window 'http://127.0.0.1:8080/trade'"
    appscript.app('Terminal').do_script(script_2)  # or any other command you choose

startCryptoBot()
time.sleep(5)
startGUI()