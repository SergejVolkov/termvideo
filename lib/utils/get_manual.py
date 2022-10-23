import io


manuals_dir = "manuals/"


def get_manual(name: str = "usage"):
    """
    Get manual page.

    Args:
        name (str): Name of the manual page.
            Defaults to "usage".

    Returns:
        str: Manual page.

    """
    with io.open(manuals_dir + name + ".man", mode="r") as m:
        return "".join(m.readlines())
