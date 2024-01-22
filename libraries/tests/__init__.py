import os, shutil


def copyFolder():
    if os.path.exists('reports/backup/allure-result'):
        shutil.rmtree('reports/backup/allure-result')

    shutil.copytree('reports/allure-result', 'reports/backup/allure-result')

def cleanUpFolder(strAbsPath = '', strFolder = ''):
    arrAllFiles = os.listdir(os.path.abspath(f'./{strAbsPath}'))
    if strFolder not in arrAllFiles:
        os.mkdir('./' + strFolder)
    folderPath = os.path.abspath(f'./{strAbsPath}' + strFolder) 
    arrFiles = os.listdir(folderPath)
    for item in arrFiles:
        arrFiles = folderPath + '\\' + item
        os.remove(arrFiles)


def forceDeleteFolder(strFolderPath):
    try:
        shutil.rmtree(strFolderPath)
    except OSError as e:
        print(f"Error deleting folder '{strFolderPath}': {e}")
        

copyFolder()
cleanUpFolder('reports/', 'allure-result')