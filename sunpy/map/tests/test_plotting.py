"""
Test Generic Map
"""
import os

import matplotlib.colors as mcolor
import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.figure import Figure

import astropy.units as u
from astropy.coordinates import SkyCoord

import sunpy
import sunpy.coordinates
import sunpy.data.test
import sunpy.map
from sunpy.coordinates import HeliographicStonyhurst
from sunpy.tests.helpers import figure_test, fix_map_wcs
from sunpy.util.exceptions import SunpyDeprecationWarning, SunpyUserWarning

testpath = sunpy.data.test.rootdir
pytestmark = pytest.mark.filterwarnings('ignore:Missing metadata')


@pytest.fixture
def aia171_test_map():
    return sunpy.map.Map(os.path.join(testpath, 'aia_171_level1.fits'))


@pytest.fixture
def heliographic_test_map():
    m = sunpy.map.Map(os.path.join(testpath, 'heliographic_phase_map.fits.gz'))
    return fix_map_wcs(m)


@pytest.fixture
def aia171_test_map_with_mask(aia171_test_map):
    shape = aia171_test_map.data.shape
    mask = np.zeros_like(aia171_test_map.data, dtype=bool)
    mask[0:shape[0] // 2, 0:shape[1] // 2] = True
    return sunpy.map.Map(np.ma.array(
        aia171_test_map.data, mask=mask),
        aia171_test_map.meta)


@figure_test
def test_plot_aia171(aia171_test_map):
    aia171_test_map.plot()


@figure_test
def test_plot_rotated_aia171(aia171_test_map):
    # Check that plotting a rotated map and a rectangle works as expected

    # Set rotation metadata
    aia171_test_map.meta['CROTA2'] = 45
    # Plot map
    aia171_test_map.plot()
    # Plot rectangle
    bottom_left = SkyCoord(
        0 * u.arcsec, 0 * u.arcsec, frame=aia171_test_map.coordinate_frame)
    w = 100 * u.arcsec
    h = 200 * u.arcsec
    aia171_test_map.draw_quadrangle(bottom_left, width=w, height=h)


@figure_test
def test_plot_aia171_clip(aia171_test_map):
    aia171_test_map.plot(clip_interval=(5., 99.)*u.percent)


@figure_test
def test_peek_aia171(aia171_test_map):
    aia171_test_map.peek()


@figure_test
def test_peek_grid_aia171(aia171_test_map):
    aia171_test_map.peek(draw_grid=True)


@figure_test
def test_peek_grid_spacing_aia171(aia171_test_map):
    aia171_test_map.peek(draw_grid=(5, 5) * u.deg)


@figure_test
def test_peek_limb_aia171(aia171_test_map):
    aia171_test_map.peek(draw_limb=True)


@figure_test
def test_draw_grid_aia171(aia171_test_map):
    aia171_test_map.plot()
    aia171_test_map.draw_grid(grid_spacing=(30, 40) * u.deg)


@figure_test
def test_peek_grid_limb_aia171(aia171_test_map):
    aia171_test_map.peek(draw_grid=True, draw_limb=True)


@figure_test
def test_plot_aia171_nowcsaxes(aia171_test_map):
    ax = plt.gca()
    with pytest.warns(SunpyDeprecationWarning, match='WCSAxes not being used as the axes'):
        aia171_test_map.plot(axes=ax)


@figure_test
def test_rectangle_aia171_width_height(aia171_test_map):
    aia171_test_map.plot()
    bottom_left = SkyCoord(
        0 * u.arcsec, 0 * u.arcsec, frame=aia171_test_map.coordinate_frame)
    w = 100 * u.arcsec
    h = 100 * u.arcsec
    aia171_test_map.draw_quadrangle(bottom_left, width=w, height=h)


@figure_test
def test_rectangle_aia171_top_right(aia171_test_map):
    aia171_test_map.plot()
    bottom_left = SkyCoord(
        0 * u.arcsec, 0 * u.arcsec, frame=aia171_test_map.coordinate_frame)
    top_right = SkyCoord(
        100 * u.arcsec, 100 * u.arcsec, frame=aia171_test_map.coordinate_frame)
    aia171_test_map.draw_quadrangle(bottom_left, top_right=top_right, label='Rectangle')
    plt.legend()  # Check that the 'Rectangle' label shows up in the legend


@figure_test
def test_quadrangle_aia17_width_height(aia171_test_map):
    aia171_test_map.plot()
    bottom_left = SkyCoord(
        50 * u.deg, -10 * u.deg, frame=HeliographicStonyhurst, obstime=aia171_test_map.date)
    w = 30 * u.deg
    h = 90 * u.deg
    aia171_test_map.draw_quadrangle(bottom_left=bottom_left, width=w, height=h)


@figure_test
def test_quadrangle_aia17_top_right(aia171_test_map):
    aia171_test_map.plot()
    bottom_left = SkyCoord(
        50 * u.deg, -10 * u.deg, frame=HeliographicStonyhurst, obstime=aia171_test_map.date)
    top_right = SkyCoord(
        65 * u.deg, 50 * u.deg, frame=HeliographicStonyhurst, obstime=aia171_test_map.date)
    aia171_test_map.draw_quadrangle(bottom_left, top_right=top_right, label='Quadrangle')
    plt.legend()  # Check that the 'Quadrangle' label shows up in the legend


@figure_test
def test_plot_masked_aia171(aia171_test_map_with_mask):
    aia171_test_map_with_mask.plot()


@figure_test
def test_plot_masked_aia171_nowcsaxes(aia171_test_map_with_mask):
    ax = plt.gca()
    with pytest.warns(SunpyDeprecationWarning, match='WCSAxes not being used as the axes'):
        aia171_test_map_with_mask.plot(axes=ax)


@figure_test
def test_plot_aia171_superpixel(aia171_test_map):
    aia171_test_map.superpixel((9, 7) * u.pix, offset=(4, 4) * u.pix).plot()


@figure_test
def test_plot_aia171_superpixel_nowcsaxes(aia171_test_map):
    ax = plt.gca()
    with pytest.warns(SunpyDeprecationWarning, match='WCSAxes not being used as the axes'):
        aia171_test_map.superpixel(
            (9, 7) * u.pix, offset=(4, 4) * u.pix).plot(axes=ax)


@figure_test
def test_plot_masked_aia171_superpixel(aia171_test_map_with_mask):
    aia171_test_map_with_mask.superpixel(
        (9, 7) * u.pix, offset=(4, 4) * u.pix).plot()


@figure_test
def test_plot_masked_aia171_superpixel_nowcsaxes(aia171_test_map_with_mask):
    ax = plt.gca()
    with pytest.warns(SunpyDeprecationWarning, match='WCSAxes not being used as the axes'):
        aia171_test_map_with_mask.superpixel(
            (9, 7) * u.pix, offset=(4, 4) * u.pix).plot(axes=ax)


@figure_test
def test_draw_contours_aia(aia171_test_map):
    aia171_test_map.plot()
    aia171_test_map.draw_contours(u.Quantity(np.arange(1, 100, 10), 'percent'))


@figure_test
def test_draw_contours_different_wcs(aia171_test_map):
    aia171_test_map._data = aia171_test_map.data.astype('float32')
    rotated_map = aia171_test_map.rotate(30*u.deg, order=3)
    rotated_map.plot()
    aia171_test_map.draw_contours(u.Quantity(np.arange(1, 100, 10), 'percent'))


@figure_test
def test_heliographic_peek(heliographic_test_map):
    heliographic_test_map.peek()


@figure_test
def test_heliographic_quadrangle_width_height(heliographic_test_map):
    heliographic_test_map.plot()
    bottom_left = SkyCoord(
        60 * u.deg, 50 * u.deg, frame=heliographic_test_map.coordinate_frame)
    w = 13 * u.deg
    h = 13 * u.deg
    heliographic_test_map.draw_quadrangle(bottom_left, width=w, height=h, edgecolor='cyan')


@figure_test
def test_heliographic_quadrangle_top_right(heliographic_test_map):
    heliographic_test_map.plot()
    bottom_left = SkyCoord(
        60 * u.deg, 50 * u.deg, frame=heliographic_test_map.coordinate_frame)
    top_right = SkyCoord(
        80 * u.deg, 90 * u.deg, frame=heliographic_test_map.coordinate_frame)
    heliographic_test_map.draw_quadrangle(bottom_left, top_right=top_right, edgecolor='cyan')


# See https://github.com/sunpy/sunpy/issues/4294 to track this warning. Ideally
# it should not be filtered, and the cause of it fixed.
@pytest.mark.filterwarnings(r'ignore:Numpy has detected that you \(may be\) writing to an array with\noverlapping memory')
@figure_test
def test_heliographic_grid_annotations(heliographic_test_map):
    heliographic_test_map.plot()
    heliographic_test_map.draw_grid(annotate=False)


def test_plot_norm_error(aia171_test_map):
    # Check that duplicating vmin, vmax raises an error
    norm = mcolor.Normalize(vmin=0, vmax=1)
    with pytest.raises(ValueError, match='Cannot manually specify vmin'):
        aia171_test_map.plot(norm=norm, vmin=0)
    with pytest.raises(ValueError, match='Cannot manually specify vmax'):
        aia171_test_map.plot(norm=norm, vmax=0)


def test_quadrangle_no_wcsaxes(aia171_test_map):
    ax = Figure().add_subplot(projection=None)  # create a non-WCSAxes plot

    bottom_left = SkyCoord(
        [0, 1] * u.arcsec, [0, 1] * u.arcsec, frame=aia171_test_map.coordinate_frame)
    with pytest.raises(TypeError, match='WCSAxes'):
        aia171_test_map.draw_quadrangle(bottom_left, axes=ax)


def test_different_wcs_plot_warning(aia171_test_map, hmi_test_map):
    aia171_test_map.plot()
    with pytest.warns(SunpyUserWarning,
                      match=(r'The map world coordinate system \(WCS\) is different '
                             'from the axes WCS')):
        hmi_test_map.plot(axes=plt.gca())
