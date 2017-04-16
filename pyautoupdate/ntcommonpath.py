###########################################################################
### CODE BELOW COPIED FROM Python 3.5.1                                 ###
### Backport of ntpath.commonpath functionality                         ###
### Modifications clearly marked via comments                           ###
### CODE USED IN COMPLIANCE WITH https://docs.python.org/3/license.html ###
###########################################################################

from ntpath import splitdrive

# Return the longest common sub-path of the sequence of paths given as input.
# The function is case-insensitive and 'separator-insensitive', i.e. if the
# only difference between two paths is the use of '\' versus '/' as separator,
# they are deemed to be equal.
#
# However, the returned path will have the standard '\' separator (even if the
# given paths had the alternative '/' separator) and will have the case of the
# first path given in the sequence. Additionally, any trailing separator is
# stripped from the returned path.

def commonpath(paths):
    """Given a sequence of path names, returns the longest common sub-path."""

    if not paths:
        raise ValueError('commonpath() arg is an empty sequence')

    if isinstance(paths[0], bytes):
        sep = b'\\'
        altsep = b'/'
        curdir = b'.'
    else:
        sep = '\\'
        altsep = '/'
        curdir = '.'

    drivesplits = [splitdrive(p.replace(altsep, sep).lower()) for p in paths]
    split_paths = [p.split(sep) for d, p in drivesplits]

    try:
        isabs, = set(p[:1] == sep for d, p in drivesplits)
    except ValueError:
        ### Begin modified block ###
        #raise ValueError("Can't mix absolute and relative paths") from None
        #raise from None is not supported in Python 2
        raise ValueError("Can't mix absolute and relative paths")
        ### End modified block ###

    # Check that all drive letters or UNC paths match. The check is made only
    # now otherwise type errors for mixing strings and bytes would not be
    # caught.
    if len(set(d for d, p in drivesplits)) != 1:
        raise ValueError("Paths don't have the same drive")

    drive, path = splitdrive(paths[0].replace(altsep, sep))
    common = path.split(sep)
    common = [c for c in common if c and c != curdir]

    split_paths = [[c for c in s if c and c != curdir] for s in split_paths]
    s1 = min(split_paths)
    s2 = max(split_paths)
    for i, c in enumerate(s1):
        if c != s2[i]:
            common = common[:i]
            break
    else:
        common = common[:len(s1)]

    prefix = drive + sep if isabs else drive
    return prefix + sep.join(common)
