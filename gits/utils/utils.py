import sys


def progress(count, total, finished_message):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = 100.0 * count / float(total)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stderr.write('[%s] %3.7f%%\r' % (bar, percents))
    sys.stderr.flush()

    if(count == total):
        print("\n{}".format(finished_message))
        return


def debug_trace():
    from PyQt5.QtCore import pyqtRemoveInputHook

    from pdb import set_trace
    pyqtRemoveInputHook()
    set_trace()
