import sys


def progress(count, total):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = 100.0 * count / float(total)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stderr.write('[%s] %3.7f%%\r' % (bar, percents))
    sys.stderr.flush()
