import numpy as np
from typhon.collocations import collapse, Collocator, expand
import xarray as xr


class TestCollocations:
    """Testing the collocation functions."""

    # refdir = join(dirname(__file__), 'reference')

    def test_flat_to_main_coord(self):
        """Tests Collocator._flat_to_main_coord

        This method is crucial since it stacks the whole input datasets for the
        collocating routine and makes them collocateable.
        """
        collocator = Collocator()

        test = xr.Dataset({
            "time": ("time", np.arange(10)),
            "lat": ("time", np.arange(10)),
            "lon": ("time", np.arange(10)),
        })
        check = xr.Dataset({
            "time": ("collocation", np.arange(10)),
            "lat": ("collocation", np.arange(10)),
            "lon": ("collocation", np.arange(10)),
        })
        results = collocator._flat_to_main_coord(test)
        assert check.equals(results)

        test = xr.Dataset({
            "time": ("main", np.arange(10)),
            "lat": ("main", np.arange(10)),
            "lon": ("main", np.arange(10)),
        })
        check = xr.Dataset({
            "time": ("collocation", np.arange(10)),
            "lat": ("collocation", np.arange(10)),
            "lon": ("collocation", np.arange(10)),
        })
        results = collocator._flat_to_main_coord(test)
        assert check.equals(results)

        test = xr.Dataset({
            "time": ("scnline", np.arange(5)),
            "lat": (("scnline", "scnpos"), np.arange(10).reshape(5, 2)),
            "lon": (("scnline", "scnpos"), np.arange(10).reshape(5, 2)),
        })
        check = test.stack(collocation=("scnline", "scnpos"))
        results = collocator._flat_to_main_coord(test)
        assert check.equals(results)

    def test_collocate_collapse_expand(self):
        """Test whether collocating, collapsing and expanding work"""
        collocator = Collocator()

        test = xr.Dataset({
            "time": ("time", np.arange("2000", "2010", dtype="M8[Y]")),
            "lat": ("time", np.arange(10)),
            "lon": ("time", np.arange(10)),
        })

        collocations = collocator.collocate(
            test, test, max_interval="30 days",
            max_distance="150 miles"
        )

        collapsed = collapse(collocations)
        expanded = expand(collocations)


