"""Hyper optimized contraction trees for large tensor networks and einsums.
"""
try:
    # -- Distribution mode --
    # import from _version.py generated by setuptools_scm during release
    from ._version import version as __version__
except ImportError:
    # -- Source mode --
    try:
        # use setuptools_scm to get the current version from src using git
        from setuptools_scm import get_version as _gv
        from pathlib import Path as _Path

        __version__ = _gv(_Path(__file__).parent.parent)
    except ImportError:
        # setuptools_scm is not available, use a default version
        __version__ = "0.0.0+unknown"

import functools

from . import utils
from .core import (
    ContractionTree,
    ContractionTreeCompressed,
    ContractionTreeMulti,
)
from .hypergraph import (
    HyperGraph,
    get_hypergraph,
)
from .hyperoptimizers import (
    hyper_baytune,
    hyper_choco,
    hyper_nevergrad,
    hyper_optuna,
    hyper_random,
    hyper_skopt,
)
from .hyperoptimizers.hyper import (
    HyperCompressedOptimizer,
    HyperMultiOptimizer,
    HyperOptimizer,
    ReusableHyperCompressedOptimizer,
    ReusableHyperOptimizer,
    get_hyper_space,
    hash_contraction,
    list_hyper_functions,
)
from .interface import (
    array_contract,
    array_contract_expression,
    array_contract_path,
    array_contract_tree,
    einsum,
    einsum_expression,
    einsum_tree,
    register_preset,
)
from .pathfinders import (
    path_basic,
    path_greedy,
    path_igraph,
    path_kahypar,
    path_labels,
)
from .pathfinders.path_basic import (
    GreedyOptimizer,
    OptimalOptimizer,
)
from .pathfinders.path_flowcutter import (
    FlowCutterOptimizer,
    optimize_flowcutter,
)
from .pathfinders.path_quickbb import QuickBBOptimizer, optimize_quickbb
from .plot import (
    plot_contractions,
    plot_contractions_alt,
    plot_scatter,
    plot_scatter_alt,
    plot_slicings,
    plot_slicings_alt,
    plot_tree,
    plot_tree_ring,
    plot_tree_span,
    plot_tree_tent,
    plot_trials,
    plot_trials_alt,
)
from .presets import (
    AutoHQOptimizer,
    AutoOptimizer,
    auto_hq_optimize,
    auto_optimize,
    greedy_optimize,
    optimal_optimize,
    optimal_outer_optimize,
)
from .slicer import SliceFinder
from .utils import (
    get_symbol,
    get_symbol_map,
)

UniformOptimizer = functools.partial(HyperOptimizer, optlib="random")
"""Does no gaussian process tuning by default, just randomly samples - requires
no optimization library.
"""

QuasiRandOptimizer = functools.partial(
    HyperOptimizer, optlib="chocolate", sampler="QuasiRandom"
)
"""Does no gaussian process tuning by default, just randomly samples but in a
more 'even' way than purely random - requires ``chocolate``.
"""

contract_expression = einsum_expression
"""Alias for :func:`cotengra.einsum_expression`."""

contract = einsum
"""Alias for :func:`cotengra.einsum`."""


__all__ = (
    "array_contract_expression",
    "array_contract_path",
    "array_contract_tree",
    "array_contract",
    "auto_hq_optimize",
    "auto_optimize",
    "AutoHQOptimizer",
    "AutoOptimizer",
    "contract_expression",
    "contract",
    "ContractionTree",
    "ContractionTreeCompressed",
    "ContractionTreeMulti",
    "einsum_expression",
    "einsum_tree",
    "einsum",
    "FlowCutterOptimizer",
    "get_hyper_space",
    "get_hypergraph",
    "get_symbol_map",
    "get_symbol",
    "greedy_optimize",
    "GreedyOptimizer",
    "hash_contraction",
    "hyper_baytune",
    "hyper_choco",
    "hyper_nevergrad",
    "hyper_optimize",
    "hyper_optuna",
    "hyper_random",
    "hyper_skopt",
    "HyperCompressedOptimizer",
    "HyperGraph",
    "HyperMultiOptimizer",
    "HyperOptimizer",
    "list_hyper_functions",
    "optimal_optimize",
    "optimal_outer_optimize",
    "OptimalOptimizer",
    "optimize_flowcutter",
    "optimize_quickbb",
    "path_basic",
    "path_greedy",
    "path_igraph",
    "path_kahypar",
    "path_labels",
    "plot_contractions_alt",
    "plot_contractions",
    "plot_scatter_alt",
    "plot_scatter",
    "plot_slicings_alt",
    "plot_slicings",
    "plot_tree_ring",
    "plot_tree_span",
    "plot_tree_tent",
    "plot_tree",
    "plot_trials_alt",
    "plot_trials",
    "QuasiRandOptimizer",
    "QuickBBOptimizer",
    "register_preset",
    "ReusableHyperCompressedOptimizer",
    "ReusableHyperOptimizer",
    "SliceFinder",
    "UniformOptimizer",
    "utils",
)


# add some presets


def hyper_optimize(inputs, output, size_dict, memory_limit=None, **opts):
    optimizer = HyperOptimizer(**opts)
    return optimizer(inputs, output, size_dict, memory_limit)


try:
    register_preset(
        "hyper",
        hyper_optimize,
    )
    register_preset(
        "hyper-256",
        functools.partial(hyper_optimize, max_repeats=256),
    )
    register_preset(
        "hyper-greedy",
        functools.partial(hyper_optimize, methods=["greedy"]),
    )
    register_preset(
        "hyper-labels",
        functools.partial(hyper_optimize, methods=["labels"]),
    )
    register_preset(
        "hyper-kahypar",
        functools.partial(hyper_optimize, methods=["kahypar"]),
    )
    register_preset(
        "hyper-balanced",
        functools.partial(
            hyper_optimize, methods=["kahypar-balanced"], max_repeats=16
        ),
    )
    register_preset(
        "hyper-compressed",
        functools.partial(
            hyper_optimize,
            minimize="peak-compressed",
            methods=("greedy-span", "greedy-compressed", "kahypar-agglom"),
        ),
        compressed=True,
    )
    register_preset(
        "hyper-spinglass",
        functools.partial(hyper_optimize, methods=["spinglass"]),
    )
    register_preset(
        "hyper-betweenness",
        functools.partial(hyper_optimize, methods=["betweenness"]),
    )
    register_preset(
        "flowcutter-2",
        functools.partial(optimize_flowcutter, max_time=2),
    )
    register_preset(
        "flowcutter-10",
        functools.partial(optimize_flowcutter, max_time=10),
    )
    register_preset(
        "flowcutter-60",
        functools.partial(optimize_flowcutter, max_time=60),
    )
    register_preset(
        "quickbb-2",
        functools.partial(optimize_quickbb, max_time=2),
    )
    register_preset(
        "quickbb-10",
        functools.partial(optimize_quickbb, max_time=10),
    )
    register_preset(
        "quickbb-60",
        functools.partial(optimize_quickbb, max_time=60),
    )
    register_preset(
        "greedy-compressed",
        path_greedy.greedy_compressed,
        compressed=True,
    )
    register_preset(
        "greedy-span",
        path_greedy.greedy_span,
        compressed=True,
    )
except KeyError:
    # KeyError: if reloading cotengra e.g. library entries already registered
    pass
