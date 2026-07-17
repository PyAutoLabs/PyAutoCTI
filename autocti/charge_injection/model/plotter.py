import logging
from typing import List

from autocti.charge_injection.imaging.imaging import ImagingCI
from autocti.charge_injection.fit import FitImagingCI
from autocti.charge_injection.plot import imaging_ci_plots
from autocti.charge_injection.plot import fit_ci_plots
from autocti.model.plotter import Plotter, plot_setting

from autocti import exc

logger = logging.getLogger(__name__)


class PlotterImagingCI(Plotter):
    """
    Outputs visualization of ``ImagingCI`` datasets and fits during a model fit, using the matplotlib
    function API in ``autocti.charge_injection.plot``.

    The images output are customized via the ``plots`` section of ``config/visualize.yaml``.
    """

    def dataset(self, dataset: ImagingCI, folder_suffix: str = ""):
        def should_plot(name):
            return plot_setting(section="dataset", name=name)

        output_path = self.image_path / f"dataset{folder_suffix}"

        if should_plot("subplot_dataset"):
            imaging_ci_plots.subplot_dataset(
                dataset=dataset,
                output_path=output_path,
                output_format=self.fmt,
                title_prefix=self.title_prefix,
            )

    def dataset_regions(
        self, dataset: ImagingCI, region_list: List[str], folder_suffix: str = ""
    ):
        def should_plot(name):
            return plot_setting(section="dataset", name=name)

        output_path = self.image_path / f"dataset{folder_suffix}"

        for region in region_list:
            try:
                if should_plot("subplot_dataset_regions"):
                    imaging_ci_plots.subplot_dataset_region(
                        dataset=dataset,
                        region=region,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

                if should_plot("data"):
                    imaging_ci_plots.figure_data_region(
                        dataset=dataset,
                        region=region,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

                if should_plot("data_logy"):
                    imaging_ci_plots.figure_data_region(
                        dataset=dataset,
                        region=region,
                        logy=True,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

            except (exc.RegionException, TypeError, ValueError):
                logger.info(
                    f"VISUALIZATION - Could not visualize the ImagingCI 1D {region}"
                )

        if should_plot("data_binned"):
            try:
                imaging_ci_plots.subplot_data_binned(
                    dataset=dataset,
                    output_path=output_path,
                    output_format=self.fmt,
                    title_prefix=self.title_prefix,
                )
            except (exc.PlottingException, exc.RegionException, TypeError, ValueError):
                logger.info(
                    "VISUALIZATION - Could not visualize the ImagingCI binned data"
                )

    def dataset_combined(
        self,
        dataset_list: List[ImagingCI],
        folder_suffix: str = "",
        filename_suffix: str = "",
    ):
        def should_plot(name):
            return plot_setting(section="dataset", name=name)

        output_path = self.image_path / f"dataset_combined{folder_suffix}"

        if should_plot("subplot_dataset"):
            imaging_ci_plots.subplot_dataset_list(
                dataset_list=dataset_list,
                output_path=output_path,
                output_filename=f"subplot_dataset_list{filename_suffix}",
                output_format=self.fmt,
                title_prefix=self.title_prefix,
            )

    def dataset_regions_combined(
        self,
        dataset_list: List[ImagingCI],
        region_list: List[str],
        folder_suffix: str = "",
        filename_suffix: str = "",
    ):
        def should_plot(name):
            return plot_setting(section="dataset", name=name)

        output_path = self.image_path / f"dataset_combined{folder_suffix}"

        for region in region_list:
            try:
                if should_plot("data"):
                    imaging_ci_plots.subplot_data_region_list(
                        dataset_list=dataset_list,
                        region=region,
                        output_path=output_path,
                        output_filename=f"subplot_data_list{filename_suffix}_{region}",
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

                if should_plot("data_logy"):
                    imaging_ci_plots.subplot_data_region_list(
                        dataset_list=dataset_list,
                        region=region,
                        logy=True,
                        output_path=output_path,
                        output_filename=f"subplot_data_logy_list{filename_suffix}_{region}",
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

            except (exc.RegionException, TypeError, ValueError):
                logger.info(
                    f"VISUALIZATION - Could not visualize the ImagingCI 1D {region}"
                )

    def fit(self, fit: FitImagingCI, during_analysis: bool, folder_suffix: str = ""):
        def should_plot(name):
            return plot_setting(section="fit", name=name)

        output_path = self.image_path / f"fit_dataset{folder_suffix}"

        if should_plot("subplot_fit"):
            fit_ci_plots.subplot_fit(
                fit=fit,
                output_path=output_path,
                output_format=self.fmt,
                title_prefix=self.title_prefix,
            )

        if not during_analysis:
            if should_plot("fits_fit"):
                fit_ci_plots.fits_fit(fit=fit, output_path=output_path)

    def fit_1d_regions(
        self,
        fit: FitImagingCI,
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
                    fit_ci_plots.subplot_fit_region(
                        fit=fit,
                        region=region,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

                if should_plot("data"):
                    fit_ci_plots.figure_fit_region(
                        fit=fit,
                        quantity="data",
                        region=region,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

                if should_plot("data_logy"):
                    fit_ci_plots.figure_fit_region(
                        fit=fit,
                        quantity="data",
                        region=region,
                        logy=True,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

                if should_plot("residual_map"):
                    fit_ci_plots.figure_fit_region(
                        fit=fit,
                        quantity="residual_map",
                        region=region,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

                if should_plot("residual_map_logy"):
                    fit_ci_plots.figure_fit_region(
                        fit=fit,
                        quantity="residual_map",
                        region=region,
                        logy=True,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

            except (exc.RegionException, TypeError, ValueError):
                logger.info(
                    f"VISUALIZATION - Could not visualize the ImagingCI 1D {region}"
                )

    def fit_combined(
        self,
        fit_list: List[FitImagingCI],
        during_analysis: bool,
        folder_suffix: str = "",
    ):
        def should_plot(name):
            return plot_setting(section="fit", name=name)

        output_path = self.image_path / f"fit_dataset_combined{folder_suffix}"

        if should_plot("residual_map"):
            for quantity in [
                "residual_map",
                "normalized_residual_map",
                "chi_squared_map",
            ]:
                fit_ci_plots.subplot_fit_list(
                    fit_list=fit_list,
                    quantity=quantity,
                    output_path=output_path,
                    output_format=self.fmt,
                    title_prefix=self.title_prefix,
                )

    def fit_1d_regions_combined(
        self,
        fit_list: List[FitImagingCI],
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
                    fit_ci_plots.subplot_fit_region_list(
                        fit_list=fit_list,
                        region=region,
                        quantity="data",
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

                if should_plot("data_logy"):
                    fit_ci_plots.subplot_fit_region_list(
                        fit_list=fit_list,
                        region=region,
                        quantity="data",
                        logy=True,
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

                if should_plot("residual_map"):
                    fit_ci_plots.subplot_fit_region_list(
                        fit_list=fit_list,
                        region=region,
                        quantity="residual_map",
                        output_path=output_path,
                        output_format=self.fmt,
                        title_prefix=self.title_prefix,
                    )

            except (exc.RegionException, TypeError, ValueError):
                logger.info(
                    f"VISUALIZATION - Could not visualize the ImagingCI 1D {region}"
                )
