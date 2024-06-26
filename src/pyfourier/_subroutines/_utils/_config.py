"""
Configuration subpackage.

This module contains flags to turn on and off optional modules.

This is copied from SigPy:
    
https://github.com/mikgroup/sigpy/blob/main/sigpy/config.py

"""

__all__ = ["cupy_enabled", "pytorch_enabled", "mklfft_enabled", "detect_gpu_backend"]

import warnings
import os

from importlib import util

import numba as nb
import numba.cuda

USE_CUPY = os.getenv("PYFOURIER_USE_CUPY", True)
USE_TORCH = os.getenv("PYFOURIER_USE_TORCH", True)
USE_MKLFFT = os.getenv("PYFOURIER_USE_MKLFFT", True)

cupy_enabled = USE_CUPY and util.find_spec("cupy") is not None
if cupy_enabled:
    try:
        import cupy  # noqa
    except ImportError as e:
        warnings.warn(
            f"Importing cupy failed. "
            f"For more details, see the error stack below:\n{e}"
        )
        cupy_enabled = False

# This is to catch an import error when the cudnn in cupy (system) and pytorch
# (built in) are in conflict.
pytorch_enabled = USE_TORCH and util.find_spec("torch") is not None
if pytorch_enabled is not None:
    try:
        import torch  # noqa
    except ImportError as e:
        warnings.warn(
            f"Importing Pytorch failed. "
            f"For more details, see the error stack below:\n{e}"
        )
        pytorch_enabled = False
else:
    pytorch_enabled = False


mklfft_enabled = USE_MKLFFT and util.find_spec("mkl_fft") is not None
if mklfft_enabled is not None:
    try:
        import mkl_fft  # noqa
    except ImportError as e:
        warnings.warn(
            f"Importing mkl-fft failed. "
            f"For more details, see the error stack below:\n{e}"
        )
        mklfft_enabled = False
else:
    mklfft_enabled = False


def detect_gpu_backend():
    """
    Detect if a GPU device is present and select GPU backend.

    If ``CuPy`` is installed, select it. This can support
    both ``CUDA`` and ``AMD`` devices, depending on the installed version.

    If ``CuPy`` is not installed, select ``Numba``. This require less
    dependencies but does not support ``AMD`` devices.

    Returns
    -------
    gpu_available : bool
        Whether a GPU is available or not.
    gpu_backend : str
        Type of GPU backend (``"numba"`` or ``"cupy"``).

    """
    if nb.cuda.is_available():
        gpu_available = True
        if cupy_enabled:
            gpu_backend = "cupy"
        else:
            gpu_backend = "numba"
    else:
        gpu_available = False

    return gpu_available, gpu_backend
