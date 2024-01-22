https://github.com/chris-brian-edamama-ph/edamamaApi

1. Download and Install SourceTree(https://www.sourcetreeapp.com/)
    1a. Select Bitbucket Option >> Click Next
    1b. Click Skip >> Next
    1c. Fill Name and Email(Edamama)
    1d. Click "No" button

2. Download and Install Visual Studio Code(https://code.visualstudio.com/Download)
    2a. Open your workspace Folder 
    NOTE: Do not forget to tick "TRUST THE AUTHORS OF ALL FILES...." checkbox
    2b. Click "Yes, I trust the authors...." button
 
3. Download and Install Python(latest version - https://www.python.org/downloads/)
    3a. When installing Python dont forget to tick "Add python.exe to Playwright" check box
    3b. Once successfully installed, Open CMD and enter:
        - python -V
        - where python
        - python
    3c. Check if added on the Environment variables(User variable) >> double click "Path" Variable
        - C:\Users\<userfolder> Tech\AppData\Local\Programs\Python\Python<version>\
        - C:\Users\<userfolder> Tech\AppData\Local\Programs\Python\Python<version>\Scripts\
        Note: Add manually if missing (Use "where python" to check correct folder path)
    3d. Add on Environment variable(User variable) >> Click "New..." button
        - PYTHONPATH = C:\Users\<userfolder>
     
4. Download and Add to PATH Allure(https://github.com/allure-framework/allure2/releases)
    4a. Extract downloaded folder in your C:\Program Files
    4b. Add on the Environment variables(System variable) >> double click "Path" Variable >> "New" button
        - C:\Program Files\allure-<version>\bin

5. How to create Python Virtual Machine
    Open terminal(Ctrl + `) and enter:
    5.1. Create your VM path directory: 
        - py -m venv <VMname> (py -m venv vmAPI)
    5.2. Activate you VM:
        - .\vmAPI\Scripts\activate (If error encountered - Perform Issue Encountered 1)
        Note: To deactivate - deactivate
    5.3. Install requirements.txt
        5.3a. to Install, enter (vmAPI should be activated)
            - pip install -r requirements.txt
            - python.exe -m pip install --upgrade pip (if need to update)
            Note: To generate a new requirement.txt file - pip freeze > requirements.txt

(OPTIONAL)
6. Follow Python Playwright Installation Guide - https://playwright.dev/python/docs/intro
    6a. Open terminal(Ctrl + `) and enter:
        - pip install pytest-playwright
        - playwright install

    Install VS Plugins:
    6b. Python
        Python Extension Pack
        python snippets



###########################################################################################################################################################
#                                                                   HOW TO EXECUTE TEST                                                                   #          
#       1. Click libraries\data\url.py >> uncomment your desire env to use. Example:                                                                      #
#           env = 'kpc'                                                                                                                                   #
#           env = 'gh5'                                                                                                                                   #
#           env = 'gls'                                                                                                                                   #
#       2. In your terminal type "pytest" then press "Enter"                                                                                              #
#       3. To run a report >> In your terminal type "allure serve reports/allure-result/" then press "Enter"                                              #  
###########################################################################################################################################################



Issue Encountered:
1. When activating VM (File C:\Users\Edamama Tech\Desktop\playwright(POC)\vmtest\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on
this system. For more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.)
    - Step 1. Open the Windows PowerShell as an administrator by the above method.
    - Step 2. Then type the command "Get-ExecutionPolicy" and hit Enter.
    - Step 3. Then type the command "Set-ExecutionPolicy RemoteSigned" and hit Enter.
    - Step 4. Then type the command "Y" and hit Enter.
    
2. When using allure serve (The term 'allure' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the..)
    -restart Visual Studio Code or Restart Laptop

3. PR can not push error encountered: (SourceTree)
    git -c diff.mnemonicprefix=false -c core.quotepath=false --no-optional-locks push -v --tags origin Working:Working
    remote: Login failed due to incorrect login credentials or method.
    remote: If you are unsure of which login details or login method to use, visit:
    remote: https://support.atlassian.com/bitbucket-cloud/docs/log-into-or-connect-to-bitbucket-cloud/
    fatal: Authentication failed for 'https://bitbucket.org/<FOLDER>/<REPO>.git/'

    Solution:
    1. Create PERSONAL ACCESS TOKEN(PAT) in your GIT >> note your PERSONAL ACCESS TOKEN(PAT) -- https://github.com/settings/tokens
    2. delete "passwd" file  in your \\AppData\Local\Atlassian\SourceTree
    3. Open SourceTree >> push you code >> password prompt will appear >> paste your PERSONAL ACCESS TOKEN(PAT)