# Print iterations progress
import time
import datetime
from sys import stdout

class progressbar(object):
    def __init__(self, total, description=""):
        """
        Call in a loop to create terminal progress bar
        @params:
            total       - Required  : total iterations (Int)
        """
        self.total = total
        self.start_time = time.time()
        self.iteration = 0
        self.description = description
        self.increase()

    def increase(self, info=""):
        length = 10
        if self.iteration > self.total: self.iteration = self.total
        termout = "\r["  # backrack
        if self.iteration == self.total:
            termout+= tcolors.BrightGreen + "   Finished   " + tsignals.ENDC
        else:
            # bar
            filledLength = int(length * self.iteration // self.total)
            percent = ("{0:3.0f}").format(100 * (self.iteration / float(self.total)))
            termout+= "="*(filledLength-1) + ">"*int(filledLength>=1) + percent + "%" + ' '*(length-filledLength)
        runtime = str(datetime.timedelta(seconds=int(time.time() -self.start_time)))
        termout+= "/ %s] %s"%(runtime,self.description+info)

        stdout.write(termout)
        stdout.flush()
        self.iteration += 1

    def end(self):
        # Print New Line on Complete
        self.increase()
        print("")


class tcolors:
    Black         = '\033[30m'
    BrightBlack   = '\033[90m'
    Red           = '\033[31m'  
    BrightRed     = '\033[91m'  
    Green         = '\033[32m'  
    BrightGreen   = '\033[92m'  
    Yellow        = '\033[33m'  
    BrightYellow  = '\033[93m'  
    Blue          = '\033[34m'  
    BrightBlue    = '\033[94m'  
    Magenta       = '\033[35m'  
    BrightMagenta = '\033[95m'  
    Cyan          = '\033[36m'  
    BrightCyan    = '\033[96m'  
    White         = '\033[37m'  
    BrightWhite   = '\033[97m'  

class teffects:
    Bold      = '\033[1m'
    Italic    = '\033[3m'
    Underline = '\033[4m'
    SlowBlink = '\033[5m'
    FastBlink = '\033[6m'

class tsignals:
    TITLE   = tcolors.BrightYellow+teffects.Bold+teffects.Underline
    OKBLUE  = tcolors.BrightBlue
    OKGREEN = tcolors.BrightGreen
    WARNING = tcolors.BrightYellow
    FAIL    = tcolors.BrightRed
    ENDC    = '\033[0m'
