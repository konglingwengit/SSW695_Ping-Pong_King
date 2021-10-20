from comback_0816 import start_comeback
from tennis import start_tennis
from Update_teams import main_url

while True:
    options = input("select what you want to run..."
                    "\n 1. comback "
                    "\n 2. tenns "
                    "\n 3. update team "
                    "\n press anyother key to exit. \n : ")
    try:
        opt = int(options)
    except:
        break

    if opt == 1:
        start_comeback()
    elif opt == 2:
        start_tennis()
    elif opt == 3:
        main_url()
    else:
        break
