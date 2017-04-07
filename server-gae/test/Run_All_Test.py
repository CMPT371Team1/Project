import os
import sys
return_code = os.system(
    "coverage run --branch --source=../web_apis --omit=../web_apis/Confirm_Email.py,../web_apis/Initialize_DB_Testers.py -m unittest discover -s . -p 'Test*.py'")
if return_code == 0:
    os.system("coverage  xml")
    os.system("coverage  html")
    sys.exit(0)

sys.exit(1)

