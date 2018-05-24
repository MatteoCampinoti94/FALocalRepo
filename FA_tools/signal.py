import signal
from SignalBlock import sigblock
from .log import log

def signal_handler(signum, frame):
    sigblock._pending += (signum,)
    print('\b\b  \b\b', end='', flush=True)

def sigint_block():
    log.normal('SIGNAL -> block sigint')
    sigblock.block(signal.SIGINT, handler=signal_handler)

def sigint_ublock():
    log.normal('SIGNAL -> unblock sigint')
    sigbloc.unblock(signal.SIGINT)

def sigint_check():
    if sigblock.pending(signal.SIGINT):
        log.normal('SIGNAL -> check sigint:True')
        return True
    else:
        return False

def sigint_clear():
    log.normal('SIGNAL -> clear pending singint')
    sigblock.clear()