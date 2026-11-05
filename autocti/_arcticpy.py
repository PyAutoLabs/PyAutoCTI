"""
Deferred access to arcticpy, the C++ arctic clocking code.

arcticpy ships only as source: building it needs GSL and a C++ toolchain, so it
is not a pip dependency of autocti. Importing it lazily means ``import autocti``
works without it — datasets, layouts, masks, plotting and loading results all
run — and only clocking, or the arcticpy classes autocti re-exports
(``ac.TrapInstantCapture``, ``ac.CCDPhase``, ``ac.ROE``, ...), need it.
"""

import importlib
from types import ModuleType

INSTALL_HINT = (
    "autocti needs arcticpy (the arctic CTI clocking code) for this, and it is "
    "not installed. arcticpy has no wheel on PyPI, so install it with the "
    "PyAutoLabs recipe, which builds it from source (it needs GSL and a C++ "
    "compiler):\n\n"
    "    https://github.com/PyAutoLabs/PyAutoHeart/blob/main/.github/actions/install-arcticpy/install_arcticpy.sh\n\n"
    "See the autocti installation docs for the full steps."
)

# The arcticpy names autocti re-exports as part of its own public API.
REEXPORTS = (
    "ROE",
    "ROEChargeInjection",
    "CCD",
    "CCDPhase",
    "TrapInstantCapture",
    "TrapSlowCapture",
    "TrapInstantCaptureContinuum",
    "TrapSlowCaptureContinuum",
    "PixelBounce",
)


def arcticpy() -> ModuleType:
    """
    Return the arcticpy module, importing it on first use.

    Raises
    ------
    ImportError
        If arcticpy is not installed, with the install recipe in the message.
    """
    try:
        return importlib.import_module("arcticpy")
    except ImportError as e:
        raise ImportError(INSTALL_HINT) from e


def _placeholder(name: str):
    """
    Stand-in for an arcticpy class or function when arcticpy is not installed.

    It is a real class, so type hints that name it still evaluate (PyAutoFit
    reads constructor annotations to build models), and calling it raises the
    install hint.
    """

    def __new__(cls, *args, **kwargs):
        raise ImportError(INSTALL_HINT)

    return type(name, (), {"__new__": __new__, "__module__": "arcticpy"})


def optional_import(*names: str):
    """
    Return the named arcticpy objects, or placeholders if arcticpy is missing.

    With arcticpy installed this is exactly ``from arcticpy import <names>``.
    Without it, each name is a placeholder that raises the install hint when
    called, so modules can import at load time and fail only when clocking.
    """
    try:
        module = arcticpy()
    except ImportError:
        objects = tuple(_placeholder(name) for name in names)
    else:
        objects = tuple(getattr(module, name) for name in names)
    return objects[0] if len(objects) == 1 else objects
