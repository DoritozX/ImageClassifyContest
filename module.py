def selectFolder():
    import tkinter.filedialog as filedialog
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()
    folder =filedialog.askdirectory(parent = root, title = "Select the folder")
    return folder

def selectFile():
    import tkinter.filedialog as filedialog
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()
    fileList = []
    filez = filedialog.askopenfiles(parent = root, title = 'Select the files')
    for i, v in enumerate(filez):
        fileList.append(v.name)
    return fileList

def getFileExtensionName(fileName):
    import os

    try:
        extenName = os.path.splitext(fileName)[1]
    except:
        print("ERROR:Wrong file format!")
        return -1
    else:
        return extenName

def readCsvFile(fileDir):
    import pandas as pd

    fileType = getFileExtensionName(fileDir)
    if fileType == ".csv":
        csvFile = pd.read_csv(fileDir)
        return csvFile
    elif fileType == ".tsv":
        tsvFile = pd.read_csv(fileDir, delimiter = '\t')
        return tsvFile
    else:
        return -1

def getClassesTag(dataFrame):
    tagCol = dataFrame.columns[1]
    tagList = dataFrame[tagCol].tolist()
    return tagList

