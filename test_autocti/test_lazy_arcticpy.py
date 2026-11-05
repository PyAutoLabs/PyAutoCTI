"""
``import autocti`` must work without arcticpy (cti-upkeep ruling R2).

Each check runs in a fresh interpreter with ``sys.modules["arcticpy"] = None``,
which makes every ``import arcticpy`` raise ImportError exactly as on a machine
where it is not installed.
"""

import subprocess
import sys
import textwrap

_HIDE_ARCTICPY = "import sys\nsys.modules['arcticpy'] = None\n"


def _run(body: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-c", _HIDE_ARCTICPY + textwrap.dedent(body)],
        capture_output=True,
        text=True,
    )


def test_import_autocti_works_without_arcticpy():
    result = _run("""
        import autocti as ac

        ac.Dataset1D
        ac.Layout2DCI
        ac.Mask1D
        ac.Clocker1D
        ac.CTI1D
        print("ok")
        """)

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip().endswith("ok")


def test_reexported_arcticpy_name_raises_install_hint_without_arcticpy():
    result = _run("""
        import autocti as ac

        try:
            ac.TrapInstantCapture
        except ImportError as e:
            print("raised:", e)
        """)

    assert result.returncode == 0, result.stderr
    assert "raised:" in result.stdout
    assert "install_arcticpy.sh" in result.stdout


def test_clocker_raises_install_hint_without_arcticpy():
    result = _run("""
        import autocti as ac

        try:
            ac.Clocker1D(express=2)
        except ImportError as e:
            print("raised:", e)
        """)

    assert result.returncode == 0, result.stderr
    assert "install_arcticpy.sh" in result.stdout


def test_reexports_are_the_real_arcticpy_classes():
    import arcticpy
    import autocti as ac
    from autocti._arcticpy import REEXPORTS

    for name in REEXPORTS:
        assert getattr(ac, name) is getattr(arcticpy, name)

    from autocti import TrapInstantCapture

    assert TrapInstantCapture is arcticpy.TrapInstantCapture
    assert set(REEXPORTS) <= set(dir(ac))
