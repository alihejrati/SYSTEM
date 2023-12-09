import os
import signal as sig
from signal import signal
from .basic import PYBASE

class Handler(PYBASE):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        self.pid = os.getpid()
        signal(sig.SIGUSR1, self.SIGUSR1)
        signal(sig.SIGUSR2, self.SIGUSR2)
        signal(sig.SIGALRM, self.SIGALRM)
        signal(sig.SIGCONT, self.SIGCONT)

    def pause(self):
        sig.pause()
    
    def send(self, **kwargs):
        """kill -USR1 <pid>"""
        pid = kwargs.get('pid', self.pid)
        sigcode = kwargs.get('sig', sig.SIGCONT)
        if isinstance(sigcode, str):
            sigcode = getattr(sig, sigcode)
        return os.kill(int(pid), int(sigcode))

    def SIGUSR(self, signum, stack):
        pass
    
    def SIGUSR1(self, signum, stack):
        pass
    
    def SIGUSR2(self, signum, stack):
        pass
    
    def SIGALRM(self, signum, stack):
        pass
    
    def SIGCONT(self, signum, stack):
        pass


if __name__ == '__main__':
    h = Handler()
    # h.send('66')
    print(sig.SIGUSR1)