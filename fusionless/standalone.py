"""Initialize a connection with Fusion from a standalone python prompt

The standalone Python still needs access to the BlackmagicFusion library
to initialize a connection. For pre-Fusion 8 versions you need PeyeonScript.

Examples:

    # Create a saver in an open fusion in its currently active comp
    >>> app = get_fusion()
    >>> comp = app.get_current_comp()
    >>> saver = comp.create_tool("Saver")

"""

try:
    # Fusion 8.0+ (bmd)
    import BlackmagicFusion as bmd
except ImportError:
    # Fusion pre-8.0 (eyeon)
    import PeyeonScript as bmd
    

def _get_app(app, ip=None, timeout=0.1, uuid=None):
    """Get an application using the `scriptapp` method.

    Args:
        app (str): Name of the application, eg. "Fusion"
        ip (str): The IP address of the host to connect to.
        timeout (float): Timeout for connection in seconds.
        uuid (str): The UUID of the application to connect to.

    Returns:
        The application's raw pointer.

    """

    if ip is None:
        ip = "127.0.0.1"    # localhost

    args = [app, ip, timeout]
    if uuid:
        args.append(uuid)

    app = bmd.scriptapp(*args)
    if not app:
        raise RuntimeError("Couldn't connect to application.")

    return app


def get_fusion(app="Fusion", ip="127.0.0.1", timeout=0.1, uuid=None):
    """Establish connection with an already active Fusion application.

    Args:
        app (str): Name of the application. (defaults to: "Fusion")
        ip (str): The IP address of the host to connect to.
        timeout (float): Timeout for connection in seconds.
        uuid (str): The UUID of the application to connect to.

    Returns:
        fusionless.core.Fusion: The created Fusion application

    """
    ptr = _get_app(app, ip, timeout, uuid)

    from .core import Fusion
    return Fusion(ptr)


def get_current_uuid():
    """This should only work from within the application.

    Returns:
        The unique id for the currently running application's script process
        which can be used elsewhere to connect to exactly this application.

    """
    return bmd.getappuuid()
