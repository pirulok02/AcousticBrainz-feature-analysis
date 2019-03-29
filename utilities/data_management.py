
def compute_instersection(*args):
    """Returns common elements in the iterables given

    Args:
        As many iterables as needed

    Return:
        intersection: elements common to all args

    """
    intersection = set(args[0])
    for arg in args[1:]:
        intersection = intersection & set(arg)
    return intersection


