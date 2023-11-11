import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log_time():
    crt_time = datetime.datetime.now()
    time = crt_time.strftime("%d/%m/%y %H:%M:%S")
    return "[" + time + "]"

class my_logger:
    def Startup(self, user: str, id: str):
        f_out = "{0} [INFO]: Logged in as {1} (ID: {2})\n".format(log_time() , user , id)
        p_out = "Current Time is : " + str(datetime.datetime.now()) + "\n" + u"{0} {1}[INFO]:{2} Logged in as {3} (ID: {4})".format(log_time() , bcolors.OKGREEN, bcolors.ENDC, user , id)
        with open('bot.log', 'w'):
            pass
        with open('bot.log', 'a') as f:
            f.write(f_out)
        print(p_out)
        print('-'* len(f_out)+"\n")

    def WARNING(self, message: str):
        out = log_time() + bcolors.WARNING + " [WARNING]: " + bcolors.ENDC + message
        file_out = log_time() + " [WARNING]: " + message + "\n"

        with open('bot.log', 'a') as f:
            f.write("{0}".format(file_out))
        print(out)

    def INFO(self, message: str):
        out = log_time() + bcolors.OKGREEN + " [INFO]:    " + bcolors.ENDC + message
        file_out = log_time() + " [INFO]:    " + message + "\n"

        with open('bot.log', 'a') as f:
            f.write("{0}".format(file_out))
        print(out)
    def ERROR(self, message: str):
        out = log_time() + bcolors.FAIL + " [ERROR]:   " + bcolors.ENDC + message
        file_out = log_time() + " [ERROR]:   " + message + "\n"

        with open('bot.log', 'a') as f:
            f.write("{0}".format(file_out))
        print(out)
