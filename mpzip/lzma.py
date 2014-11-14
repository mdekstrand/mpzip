import core


def _open_in(fn):
    return core.open_decompressor(['unxz'], fn)


def _open_out(fn, level, append):
    args = ['xz']
    if level == 'best':
        args.append('--best')
    elif level is not None:
        args.append('-%d' % (level,))
    return core.open_compressor(['xz'], fn, append)


def open(filename, mode='rb', level=None):
    if mode.lower() in ('r', 'rb'):
        return _open_in(filename)
    elif mode.lower() in ('w', 'wb'):
        return _open_out(filename, level, False)
    elif mode.lower() in ('a', 'ab'):
        return _open_out(filename, level, True)
    else:
        raise ValueError('invalid mode ' + mode)
