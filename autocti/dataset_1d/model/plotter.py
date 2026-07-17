import logging
from typing import List

from autocti.dataset_1d.dataset_1d.dataset_1d import Dataset1D
from autocti.dataset_1d.fit import FitDataset1D
from autocti.dataset_1d.plot import dataset_1d_plots
from autocti.dataset_1d.plot import fit_plots
from autocti.model.plotter import Plotter, plot_setting

from autocti import exc

logger = logging.getLogger(__name__)


class PlotterDataset1D(Plotter):
    """
    Outputs visualization of ``Dataset1D`` datasets and fits during a model fit, using the matplotlib
    function API in ``autocti.dataset_1d.plot``.

    The images output are customized via the ``plots`` section of ``config/visualize.yaml``.
    """

    def dataset(self, dataset: Dataset1D, folder_suffix: str = ""):
        def should_plot(name):
            return plot_setting(section="dataset", name=name)

        output_path = self.image_path / f"dataset{folder_suffix}"

        if should_plot("subplot_dataset"):
            dataset_1d_plots.subplot_dataset(
                dataset=dataset,
                output_path=output_path,
                output_format=self.fmt,
                title_prefix=self.title_prefix,
            )

        if should_plot("data"):
            dataset_1d_plots.figure_data(
                dataset=dataset,
                output_path=output_path,
                output_format=self.fmt,
                title_prefix=self.title_prefix,
            )

        if should_plot("data_logy"):
            dataset_1d_plots.figure_data(
                dataset=dataset,
                logy=True,
                output_path=output_path,
                output_format=self.fmt,
                title_prefix=self.title_prefix,
            )

    def dataset_regions(
        self, dataset: Dataset1D, region_list: List[str], folder_suffix: str = ""
    ):
        def should_plot(name):
            return plot_setting(section="dataset", name=name)

        output_path = self.image_path / f"dataset{folder_suffix}"

        for region in region_list:
            try:
                if should_plot("subplot_dataset_regions"):
                    dataset_1d_plots.subplot_dataset(
                        dataset=dataset,
                        region=region,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

                if should_plot("data"):
                    dataset_1d_plots.figure_data(
                        dataset=dataset,
                        region=region,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

                if should_plot("data_logy"):
                    dataset_1d_plots.figure_data(
                        dataset=dataset,
                        region=region,
                        logy=True,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

            except (exc.RegionException, TypeError, ValueError):
                logger.info(
                    f"VISUALIZATION - Could not visualize the Dataset1D {region}"
                )

    def dataset_combined(self, dataset_list: List[Dataset1D], folder_suffix: str = ""):
        def should_plot(name):
            return plot_setting(section="dataset", name=name)

        output_path = self.image_path / f"dataset{folder_suffix}"

        if should_plot("subplot_dataset"):
            dataset_1d_plots.subplot_dataset_list(
                dataset_list=dataset_list,
                output_path=output_path,
                output_format=self.fmt,
                title_prefix=self.title_prefix,
            )

    def dataset_regions_combined(
        self,
        dataset_list: List[Dataset1D],
        region_list: List[str],
        folder_suffix: str = "",
    ):
        def should_plot(name):
            return plot_setting(section="dataset", name=name)

        output_path = self.image_path / f"dataset{folder_suffix}"

        for region in region_list:
            try:
                if should_plot("data"):
                    dataset_1d_plots.subplot_dataset_list(
                        dataset_list=dataset_list,
                        region=region,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

                if should_plot("data_logy"):
                    dataset_1d_plots.subplot_dataset_list(
                        dataset_list=dataset_list,
                        region=region,
                        logy=True,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

            except (exc.RegionException, TypeError, ValueError):
                logger.info(
                    f"VISUALIZATION - Could not visualize the Dataset1D {region}"
                )

    def fit(self, fit: FitDataset1D, during_analysis: bool, folder_suffix: str = ""):
        def should_plot(name):
            return plot_setting(section="fit", name=name)

        output_path = self.image_path / f"fit_dataset{folder_suffix}"

        if should_plot("subplot_fit"):
            fit_plots.subplot_fit(
                fit=fit,
                output_path=output_path,
                output_format=self.fmt,
                title_prefix=self.title_prefix,
            )

        if should_plot("data"):
            fit_plots.figure_fit(
                fit=fit,
                quantity="data",
                output_path=output_path,
                output_format=self.fmt,
                title_prefix=self.title_prefix,
            )

        if should_plot("data_logy"):
            fit_plots.figure_fit(
                fit=fit,
                quantity="data",
                logy=True,
                output_path=output_path,
                output_format=self.fmt,
                title_prefix=self.title_prefix,
            )

        if should_plot("residual_map"):
            fit_plots.figure_fit(
                fit=fit,
                quantity="residual_map",
                output_path=output_path,
                output_format=self.fmt,
                title_prefix=self.title_prefix,
            )

        if should_plot("residual_map_logy"):
            fit_plots.figure_fit(
                fit=fit,
                quantity="residual_map",
                logy=True,
                output_path=output_path,
                output_format=self.fmt,
                title_prefix=self.title_prefix,
            )

        if not during_analysis:
            if should_plot("fits_fit"):
                fit_plots.fits_fit(fit=fit, output_path=output_path)

    def fit_regions(
        self,
        fit: FitDataset1D,
        region_list: List[str],
        during_analysis: bool,
        folder_suffix: str = "",
    ):
        def should_plot(name):
            return plot_setting(section="fit", name=name)

        output_path = self.image_path / f"fit_dataset{folder_suffix}"

        for region in region_list:
            try:
                if should_plot("subplot_fit_regions"):
                    fit_plots.subplot_fit(
                        fit=fit,
                        region=region,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

                if should_plot("data"):
                    fit_plots.figure_fit(
                        fit=fit,
                        quantity="data",
                        region=region,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

                if should_plot("data_logy"):
                    fit_plots.figure_fit(
                        fit=fit,
                        quantity="data",
                        region=region,
                        logy=True,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

            except (exc.RegionException, TypeError, ValueError):
                logger.info(
                    f"VISUALIZATION - Could not visualize the Dataset1D {region}"
                )

    def fit_combined(
        self,
        fit_list: List[FitDataset1D],
        during_analysis: bool,
        folder_suffix: str = "",
    ):
        def should_plot(name):
            return plot_setting(section="fit", name=name)

        output_path = self.image_path / f"fit_dataset_combined{folder_suffix}"

        for quantity, key in [
            ("data", "data"),
            ("residual_map", "residual_map"),
            ("normalized_residual_map", "residual_map"),
            ("chi_squared_map", "residual_map"),
        ]:
            if should_plot(key):
                fit_plots.subplot_fit_list(
                    fit_list=fit_list,
                    quantity=quantity,
                    output_path=output_path,
                    output_format=self.fmt,
                    title_prefix=self.title_prefix,
                )

    def fit_region_combined(
        self,
        fit_list: List[FitDataset1D],
        region_list: List[str],
        during_analysis: bool,
        folder_suffix: str = "",
    ):
        def should_plot(name):
            return plot_setting(section="fit", name=name)

        output_path = self.image_path / f"fit_dataset_combined{folder_suffix}"

        for region in region_list:
            try:
                if should_plot("data"):
                    fit_plots.subplot_fit_list(
                        fit_list=fit_list,
                        quantity="data",
                        region=region,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

                if should_plot("data_logy"):
                    fit_plots.subplot_fit_list(
                        fit_list=fit_list,
                        quantity="data",
                        region=region,
                        logy=True,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

                if should_plot("residual_map"):
                    fit_plots.subplot_fit_list(
                        fit_list=fit_list,
                        quantity="residual_map",
                        region=region,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

            except (exc.RegionException, TypeError, ValueError):
                logger.info(
                    f"VISUALIZATION - Could not visualize the Dataset1D {region}"
                )
