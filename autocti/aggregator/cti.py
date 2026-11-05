from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional, Union

from autocti.aggregator.abstract import AggBase
from autocti.aggregator.abstract import _cti_list_from

if TYPE_CHECKING:
    from autocti.model.model_util import CTI1D
    from autocti.model.model_util import CTI2D

import autofit as af


def _cti_from(
    fit: af.Fit, instance: Optional[af.ModelInstance] = None
) -> Union[CTI1D, CTI2D, List[Union[CTI1D, CTI2D]]]:
    """
    Returns the `CTI` model(s) of a `PyAutoFit` sqlite database `Fit` object.

    The results of a model-fit can be stored in a sqlite database, including the model and its best fit
    parameters (e.g. `model.json`), which this function turns back into `CTI` objects for a given non-linear
    search sample (e.g. the maximum likelihood model).

    A fit to a single dataset returns one `CTI` object. A fit to multiple datasets, made with a
    `FactorGraphModel`, has one child instance per dataset, and returns a list with one `CTI` object per dataset
    (in the same order as the datasets were fitted), as the fit aggregators do.

    Parameters
    ----------
    fit
        A PyAutoFit database Fit object containing the generators of the results of model-fits.
    instance
        A manual instance that overwrites the max log likelihood instance in fit (e.g. for drawing the instance
        randomly from the PDF).

    Returns
    -------
    The `CTI` model, or the list of `CTI` models of a multi-dataset fit.
    """
    instance = instance if instance is not None else fit.instance

    if not fit.children:
        return instance.cti

    return _cti_list_from(source=instance, total_datasets=len(fit.children))


class CTIAgg(AggBase):
    """
    Interfaces with an `PyAutoFit` aggregator object to create instances of `CTI` objects from the results
    of a model-fit.

    The results of a model-fit can be stored in a sqlite database, including the following attributes of the fit:

    - The model and its best fit parameters (e.g. `model.json`).

    The `aggregator` contains the path to each of these files, and they can be loaded individually. This class
    can load them all at once and create an `CTI` object via the `_cti_from` method.

    This class's methods returns generators which create the instances of the `CTI` objects. This ensures
    that large sets of results can be efficiently loaded from the hard-disk and do not require storing all
    `CTI` instances in the memory at once.

    For example, if the `aggregator` contains 3 model-fits, this class can be used to create a generator which
    creates instances of the corresponding 3 `CTI` objects.

    A fit to a single dataset gives one `CTI` object per fit. A fit to multiple datasets at once, made with a
    `FactorGraphModel`, gives a list with one `CTI` object per dataset (in the order the datasets were fitted).

    This can be done manually, but this object provides a more concise API.

    Parameters
    ----------
    aggregator
        A `PyAutoFit` aggregator object which can load the results of model-fits.
    """

    def object_via_gen_from(
        self, fit, instance: Optional[af.ModelInstance] = None
    ) -> Union[CTI1D, CTI2D, List[Union[CTI1D, CTI2D]]]:
        """
        Returns the `CTI` object(s) of a model-fit in the aggregator.

        See `__init__` for a description of how the `CTI` objects are created by this method.

        Parameters
        ----------
        fit
            A `PyAutoFit` `Fit` object which contains the results of a model-fit as an entry in a sqlite database.
        instance
            A manual instance that overwrites the max log likelihood instance in fit (e.g. for drawing the instance
            randomly from the PDF).

        Returns
        -------
        The `CTI` object whose parameters are a sample of the non-linear search, or for a multi-dataset
        (`FactorGraphModel`) fit a list with one `CTI` object per dataset.
        """
        return _cti_from(fit=fit, instance=instance)
