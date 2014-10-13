# Use 'final' as the 4th element to indicate
# a full release

VERSION = (0, 1, 0, 'alpha', 1)


def get_short_version():
    return '%s.%s' % (VERSION[0], VERSION[1])


def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    # Append 3rd digit if > 0
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    elif VERSION[3] != 'final':
        version = '%s %s' % (version, VERSION[3])
        if len(VERSION) == 5:
            version = '%s %s' % (version, VERSION[4])
    return version
