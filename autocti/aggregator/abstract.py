from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from autocti.clocker.abstract import AbstractClocker

import autofit as af


class AggBase(af.AggBase):
    def __init__(
        self,
        aggregator: af.Aggregator,
        use_dataset_full: bool = False,
        clocker_list: Optional[List[AbstractClocker]] = None,
    ):
        """
        An abstract aggregator wrapper, which makes it straight forward to compute generators of objects from specific
        samples of a non-linear search.

        For example, in **PyAutoLens**, this makes it straight forward to create generators of `Plane`'s drawn from
        the PDF estimated by a non-linear for efficient error calculation of derived quantities.
        Parameters
        ----------
        aggregator
            An PyAutoFit aggregator containing the results of non-linear searches performed by PyAutoFit.
        clocker
            The CTI arctic clocker used by aggregator's instances. If None is input, the clocker used by the
            non-linear search and model-fit is used.
        """
        super().__init__(aggregator=aggregator)

        self.use_dataset_full = use_dataset_full
        self.clocker_list = clocker_list


def _cti_list_from(source, total_datasets: int):
    """
    Extract one CTI model per dataset from a model instance.

    A single-analysis instance exposes ``instance.cti`` directly; a factor-graph
    instance (multi-dataset fit) is an indexed collection with one child
    instance per factor.
    """
    if hasattr(source, "cti"):
        return [source.cti] * total_datasets

    # A factor-graph instance also carries the FactorGraphModel itself as a
    # trailing child, so only children with a CTI model are taken.
    cti_list = [child.cti for child in source if hasattr(child, "cti")]

    if len(cti_list) != total_datasets:
        raise ValueError(
            f"The instance contains {len(cti_list)} CTI models but the fit has "
            f"{total_datasets} datasets."
        )

    return cti_list
