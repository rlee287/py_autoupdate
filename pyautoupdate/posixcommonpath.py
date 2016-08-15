###########################################################################
### CODE BELOW COPIED FROM Python 3.5.1                                 ###
### Backport of posixpath.commonpath functionality                      ###
### Modifications clearly marked via comments                           ###
### CODE USED IN COMPLIANCE WITH https://docs.python.org/3/license.html ###
###########################################################################


# Return the longest common sub-path of the sequence of paths given as input.
# The paths are not normalized before comparing them (this is the
# responsibility of the caller). Any trailing separator is stripped from the
# returned path.

def commonpath(paths):
    """Given a sequence of path names, returns the longest common sub-path."""

    if not paths:
        raise ValueError('commonpath() arg is an empty sequence')

    if isinstance(paths[0], bytes):
        sep = b'/'
        curdir = b'.'
    else:
        sep = '/'
        curdir = '.'

    split_paths = [path.split(sep) for path in paths]
    
    try:
        isabs, = set(p[:1] == sep for p in paths)
    except ValueError:
        ### Begin modified block
        #raise ValueError("Can't mix absolute and relative paths") from None
        #raise from None is not supported in Python 2
        raise ValueError("Can't mix absolute and relative paths")
        ### End modified block
    split_paths = [[c for c in s if c and c != curdir] for s in split_paths]
    s1 = min(split_paths)
    s2 = max(split_paths)
    common = s1
    for i, c in enumerate(s1):
        if c != s2[i]:
            common = s1[:i]
            break

    prefix = sep if isabs else sep[:0]
    return prefix + sep.join(common)
