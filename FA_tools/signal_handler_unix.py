import signal

def sigint_block():
    signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGINT})

def sigint_ublock():
    signal.pthread_sigmask(signal.SIG_UNBLOCK, {signal.SIGINT})

def sigint_check():
    if signal.SIGINT in signal.sigpending():
        return True
    else:
        return False