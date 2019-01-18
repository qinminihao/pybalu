__all__ = ['fourier', 'FourierExtractor']

import numpy as np
from scipy.misc import imresize
import itertools as it

from ._feature_extractor import FeatureExtractorBase

def fourier(image, region=None, *, vresize=64, hresize=64, vfreq=2, hfreq=2, show=False, labels=False):
    '''\
fourier(image, region=None, *, vresize=64, hresize=64, vfreq=2, hfreq=2, show=False, labels=False)

Return an array of with the fourier features extracted from an image given resize and frequency
values.

Parameters
----------
image : a numpy 2 dimensional float array
    It represents a grayscale image or just one dimension of color (eg: green channel)
region : a numpy 2 dimensional array, optional
    A ndarray of the same dimensions as `image` of boolean type. All pixels not set to
    true on this array, will be set to 0 on `image` before resizing and sampling.
    if not given, no pixels will be modified before resizing and sampling.
vresize: int, optional
    `image` will be resized to this height before sampling. Default is 64
hresize: int, optional
    `image` will be resized to this width before sampling. Default is 64
vfreq: int, optional
    Vertical sampling frequency. Default is 2
hfreq: int, optional
    Horizontal sampling frequency. Default is 2
show : bool, optional
    Wether to print or not messages during execution
labels : bool, optional
    Wether to return a second array that contains the label of each value. 

Returns
-------
labels: ndarray, optional
    A one dimensional string ndarray that contains the labels to each of the features.
    This array is only returned if `labels` is set to True.
features: ndarray
    A float ndarray that contains 2 * `vfreq` * `hfreq` features extracted from `image`
    after its resize.

See Also
--------
clp : <Not Implemented Yet>
dct : <Not Implemented Yet>
fourier_des : Extracts the fourier descriptors of an image.
gabor : ( TODO )
haralick : Extracts 28 haralick texture features from an image.
lbp : ( TODO )

Examples
--------
Load an image on its grayscale representation, then proceed to get its features:

>>> from pybalu.feature_extraction import fourier
>>> from pybalu.misc import imread
>>> img = imread('testimg.png', flatten=True) # to grayscale
>>> features = fourier(img)

Print a binary image features:

>>> from pybalu.IO import print_features
>>> labels, features = fourier(img, labels=True)
>>> print_features(labels, features)
Fourier Abs (1, 1)      :  6948.20449
Fourier Abs (1, 2)      :  966.09909
Fourier Abs (2, 1)      : -148.03935
Fourier Abs (2, 2)      :  92.26226
Fourier Ang (1, 1) [rad]: -0.13091
Fourier Ang (1, 2) [rad]:  0.07754
Fourier Ang (2, 1) [rad]:  0.12337
Fourier Ang (2, 2) [rad]:  0.01847
'''

    if region is None:
        region = np.ones_like(image)
    
    I = image.astype(float)
    I[region == 0] = 0
    
    v_half = round(vresize / 2) + 1
    h_half = round(hresize / 2) + 1

    if show:
        print('--- extracting Fourier features...')

    img_resize = imresize(I, (vresize, hresize), interp='bicubic', mode='F')
    img_fourier = np.fft.fft2(img_resize)
    img_abs = np.abs(img_fourier)
    img_angle = np.angle(img_fourier)

    F = imresize(img_abs[:v_half, :h_half], (vfreq, hfreq), interp='bicubic', mode='F')
    A = imresize(img_angle[:v_half, :h_half], (vfreq, hfreq), interp='bicubic', mode='F')

    features = np.hstack([F.ravel(), A.ravel()]).astype(float)
    if labels:
        fourier_labels = np.zeros(vfreq * hfreq * 2, dtype='<U28')
        fourier_labels[:vfreq * hfreq] = [f'Fourier Abs ({i}, {j})' for i, j in \
                                          it.product(range(1, vfreq+1), range(1, hfreq+1))]
        fourier_labels[vfreq * hfreq:] = [f'Fourier Ang ({i}, {j}) [rad]' for i, j in \
                                          it.product(range(1, vfreq+1), range(1, hfreq+1))]
        return fourier_labels, features
    return features

class FourierExtractor(FeatureExtractorBase):
    extractor_func = fourier