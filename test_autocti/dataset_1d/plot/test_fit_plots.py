from pathlib import Path

import pytest

import autocti.plot as aplt

directory = Path(__file__).resolve().parent


@pytest.fixture(name="plot_path")
def make_plot_path():
    return directory / "files" / "plots"


def test__figure_fit(fit_1d_7, plot_path, plot_patch):
    aplt.figure_fit_dataset_1d(
        fit=fit_1d_7, quantity="data", output_path=plot_path, output_format="png"
    )
    aplt.figure_fit_dataset_1d(
        fit=fit_1d_7,
        quantity="residual_map",
        region="eper",
        logy=True,
        output_path=plot_path,
        output_format="png",
    )
    aplt.figure_fit_dataset_1d(
        fit=fit_1d_7,
        quantity="chi_squared_map",
        output_path=plot_path,
        output_format="png",
    )

    assert str(Path(plot_path) / "data.png") in plot_patch.paths
    assert str(Path(plot_path) / "residual_map_logy_eper.png") in plot_patch.paths
    assert str(Path(plot_path) / "chi_squared_map.png") in plot_patch.paths


def test__subplot_fit(fit_1d_7, plot_path, plot_patch):
    aplt.subplot_fit_dataset_1d(
        fit=fit_1d_7, output_path=plot_path, output_format="png"
    )
    aplt.subplot_fit_dataset_1d(
        fit=fit_1d_7, region="fpr", output_path=plot_path, output_format="png"
    )

    assert str(Path(plot_path) / "subplot_fit.png") in plot_patch.paths
    assert str(Path(plot_path) / "subplot_fit_fpr.png") in plot_patch.paths


def test__subplot_fit_list(fit_1d_7, plot_path, plot_patch):
    aplt.subplot_fit_dataset_1d_list(
        fit_list=[fit_1d_7, fit_1d_7],
        quantity="residual_map",
        output_path=plot_path,
        output_format="png",
    )

    assert str(Path(plot_path) / "subplot_residual_map_list.png") in plot_patch.paths


def test__fits_fit(fit_1d_7, plot_path, tmp_path):
    aplt.fits_fit_dataset_1d(fit=fit_1d_7, output_path=tmp_path)

    assert (Path(tmp_path) / "fit.fits").exists()


def test__fits_fit__creates_missing_output_directory(fit_1d_7, tmp_path):
    # Under PYAUTO_FAST_PLOTS=1 no figure is saved first, so nothing else has
    # created the fit's image subfolder when the FITS file is written.
    from autocti.dataset_1d.plot.fit_plots import fits_fit

    output_path = tmp_path / "image" / "fit_dataset"

    fits_fit(fit=fit_1d_7, output_path=output_path)

    assert (output_path / "fit.fits").is_file()
