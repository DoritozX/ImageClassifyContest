#-*- coding: UTF-8 -*-]
import os
import inspect
import sys
import time
import logging
import traceback
import datetime

class ErrorLog :
    """
     Usage£º
? ? ? ? Define logger = ErrorLog(ErrorLog.rename()) in the first of function
? ? ? ? And use logger.error("Error Messages") in exception process
    """

    #The size limit of error log
    size_limit = 1000000

    def __init__(self,logger):
        self.errTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
        self.fileHandlerName = ''
        self.fileHandler = None
        self.loggerName = logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        self.fileName = os.path.abspath(os.curdir) + "\\" + "ErrorLog" + "\\" + time.strftime("ErrLog%Y%m%d") + '.log'
        #Assign the fomat of log£º
        #Time¡¢log name¡¢log level¡¢file name¡¢function name¡¢row number¡¢user messages
        self.formatter = logging.Formatter(self.errTime + "\%(filename)s\%(name)s,%(lineno)d ,%(message)s")
        #Define a streamHandler
        ch = logging.StreamHandler()
        #If log level is over the "DEBUG", the print it in the console
        ch.setLevel(logging.DEBUG)
        #Output the error log with the format assigned
        ch.setFormatter(self.formatter)
        #self.logger.addHandler(ch)

        #self.fileHandlerName = fname
        #self.fileHandler = fh
    def setfh(self):
        fname = time.strftime("ErrLog%Y%m%d")
        if fname != self.fileHandlerName:
        #If the file name is different with the handle name, then drop the handle name
            if self.fileHandler != None :
                self.logger.removeHandler(self.fileHandler)
            #The path of error log folder
            path = os.path.abspath(os.curdir) + "\\" + "ErrorLog" + "\\"
            #print(path)
            #Create the folder when it not exists
            the_file = path + fname + '.log'
            if os.path.isdir(path) == False:
                os.makedirs(path)
            #Check whether the log file exist
            if os.path.isfile(the_file) == True :
                #Get the size of log file
                size = os.path.getsize(the_file)
                #If the size is over the limit size, then delete it
                if size > self.size_limit :
                    os.remove(the_file)

            #Save the file
            fh = logging.FileHandler(the_file)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(self.formatter)
            self.fileHandlerName = fname
            self.fileHandler = fh
            self.logger.addHandler(fh)

    #def setfh_by_size(self) :
    #? ? fname = "ErrLog"
    #? ? if fname != self.fileHandlerName :
    #? ? ? ? self.logger.removeHandler(self.fileHandler)
    #? ? path =
    #? ? os.path.abspath(os.path.dirname("C:\\Users\\215012\\Desktop\\R\\Python\\CM_calculate_test\\"))
    #? ? + "\\" + "ErrorLog" + "\\"
    #? ? print(path)


    #Fomat the contents of the error log
    def _fmtInfo(self,msg):
        #If there is no user messages, then use the stack trace messages
        if len(msg) == 0:
            msg = traceback.format_exc()
            return msg
        #If there are user messages, then append the stack trace messages after it
        else:
            _tmp = [msg[0]]
            _tmp.append(traceback.format_exc())
            return _tmp[0]
    #Error level
    #In most situations, use error()
    def debug(self,*msg):
        _info = self._fmtInfo(msg)
        try :
            self.setfh()
            self.logger.debug(_info)
            #self.fileHandler = (_info)
        except :
            print("mylog debug:" + _info)
    def error(self,*msg):
        _info = self._fmtInfo(msg)
        try :
            self.setfh()
            self.logger.error(_info)
        except :
            print("mylog error:" + _info)
    def info(self,*msg):
        _info = self._fmtInfo(msg)
        try :
            self.setfh()
            self.logger.error(_info)
        except :
            print("mylog info:" + _info)
    def warning(self,*msg):
        _info = self._fmtInfo(msg)
        try :
            self.setfh()
            self.logger.error(_info)
        except :
            print("mylog warning:" + _info)

    def rename() :
        func = inspect.stack()[1][3]
        length = 35
        if len(func) < length :
            for i in range(length - len(func)) :
                func = func + " "
        else:
            print("The function name is too long.")
            pass

        return func

    def reverse_file(self) :
        text = []
        print(self.fileName)
        file = open(self.fileName, "r+")
        text_list = file.readlines()

        for m in text_list:
            print (m + "\n")
        print ("#############################")
        if len(text_list) <= 0 :
            return

        b = text_list[len(text_list)-1][11:25]
        for i in text_list:
            a = i[11:25]
            if a == b :
                text.append(i)
                del text_list[text_list.index(i)]
        for j in text:
            text_list.insert(0, j)
        for k in text_list :
            print (k + "\n")
        file.seek(0)
        file.truncate()
        file.writelines(text_list)
        file.close()
