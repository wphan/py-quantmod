"""High-level functions meant for user access

This includes various plotting and theming helpers.
Module also contains all argument validity checks.

"""
from __future__ import absolute_import

import six
import copy

from . import auth
from . import utils
from .theming.skeleton import SKELETON
from .theming.themes import THEMES


_VALID_BASE_COMPONENTS = {'base_colors', 'base_traces',
                          'base_additions', 'base_layout'}

_VALID_THEME_COMPONENTS = {'colors', 'traces', 'additions', 'layout'}

_VALID_COLORS = {'increasing', 'decreasing',
                 'primary', 'secondary', 'tertiary',
                 'grey', 'grey_light', 'grey_strong',
                 'fill', 'fill_light', 'fill_strong',
                 'fillcolor'}

_VALID_TRACES = {'candlestick',
                 'line', 'line_thin', 'line_thick', 'line_dashed',
                 'line_dashed_thin', 'line_dashed_thick',
                 'area', 'area_dashed', 'area_threshold',
                 'scatter', 'bar', 'histogram'}

_VALID_ADDITIONS = {'xaxis', 'yaxis'}

_VALID_LAYOUT = {'title', 'width', 'height', 'autosize',
                 'font', 'margin', 'hovermode',
                 'plot_bgcolor', 'paper_bgcolor',
                 'showlegend', 'legend'}

_VALID_TEMPLATE_KWARGS = {'figsize'}  # Matplotlib/Cufflinks syntax


def get_theme(theme):
    """Return a Quantmod theme (as a dict).

    Parameters
    ----------
        theme : string
            Quantmod theme

    """
    if theme in THEMES:
        return copy.deepcopy(THEMES[theme])
    else:
        raise Exception("Invalid theme '{0}'.".format(theme))


def get_themes():
    """Return the list of available themes, or none if there is a problem."""
    return list(THEMES)


def get_skeleton():
    """Return the base Quantmod skeleton."""
    return copy.deepcopy(SKELETON)


def make_colors(base_colors, colors):
    """Make trace configuration from theme/skeleton and theme/colors.

    Recursively update base_theme with theme using custom tool in utils.

    Parameters
    ----------
        base_colors : dict
            Additions file containing primitives from 'skeleton.py'.
        colors : dict
            Additions configuration from specified theme.

    """
    for key in colors:
        if key not in _VALID_COLORS:
            raise Exception("Invalid keyword '{0}'".format(key))

    def _expand(base_colors):
        pass

    _expand(base_colors)

    # Modifiers directly to base_colors
    utils.update(base_colors, colors)

    for key in base_colors:
        if key not in _VALID_COLORS:
            raise Exception("Invalid keyword '{0}'".format(key))

    return base_colors


def make_traces(base_traces, traces):
    """Make trace configuration from theme/skeleton and theme/traces.

    Recursively update base_theme with theme using custom tool in utils.

    Parameters
    ----------
        base_traces : dict
            Trace file containing primitives from 'skeleton.py'.
        traces : dict
            Trace configuration from specified theme.

    """
    # Check for invalid entries
    for key in traces:
        if key not in _VALID_TRACES:
            raise Exception("Invalid keyword '{0}'".format(key))

    def _expand(base_traces):
        """Creates other traces from the three elementary ones."""
        base_traces['candlestick']

        base_traces['line']
        base_traces['line_thin'] = copy.deepcopy(base_traces['line'])
        base_traces['line_thick'] = copy.deepcopy(base_traces['line'])
        base_traces['line_dashed'] = copy.deepcopy(base_traces['line'])
        base_traces['line_dashed_thin'] = copy.deepcopy(base_traces['line'])
        base_traces['line_dashed_thick'] = copy.deepcopy(base_traces['line'])

        base_traces['area'] = copy.deepcopy(base_traces['line'])
        base_traces['area']['fill'] = 'tonexty'
        base_traces['area_dashed'] = copy.deepcopy(base_traces['area'])
        base_traces['area_threshold'] = copy.deepcopy(base_traces['area'])

        base_traces['scatter'] = copy.deepcopy(base_traces['line'])
        base_traces['scatter']['mode'] = 'markers'

        base_traces['bar']
        base_traces['histogram'] = copy.deepcopy(base_traces['bar'])

    _expand(base_traces)

    # Mdifiers currently to 'line' only
    # This may be subject to laterchange
    for key in traces:
        utils.update(base_traces[key]['line'], traces[key])

    # Check after copying
    for key in base_traces:
        if key not in _VALID_TRACES:
            raise Exception("Invalid keyword '{0}'".format(key))

    return base_traces


def make_additions(base_additions, additions):
    """Make trace configuration from theme/skeleton and theme/additions.

    Recursively update base_theme with theme using custom tool in utils.

    Parameters
    ----------
        base_additions : dict
            Additions file containing primitives from 'skeleton.py'.
        additions : dict
            Additions configuration from specified theme.

    """
    for key in additions:
        if key not in _VALID_ADDITIONS:
            raise Exception("Invalid keyword '{0}'".format(key))

    # No utility right now, planned in the future for additions
    def _expand(base_additions):
        pass

    _expand(base_additions)

    # Modifiers directly to base_additions
    utils.update(base_additions, additions)

    for key in base_additions:
        if key not in _VALID_ADDITIONS:
            raise Exception("Invalid keyword '{0}'".format(key))

    return base_additions


def make_layout(base_layout, layout, custom_layout,
                legend, hovermode,
                annotations, shapes, title,
                dimensions, width, height, margin, **kwargs):
    """Make layout configuration from theme/skeleton and theme/traces.

    Recursively update base_theme with theme using custom tool in utils.

    Parameters
    ----------
        base_traces : dict
            Layout file containing primitives from 'skeleton.py'.
        layout : dict
            Layout configuration from specified theme.
        custom_layout : dict
            Plotly layout dict or graph_objs.Layout object.
            Will override all other arguments if conflicting as
            user-inputted layout is updated last.
        legend : dict or bool
            True/False or Plotly legend dict / graph_objs.Legend object.
            If legend is a bool, Quantmod will simply toggle legend visibility.
        hovermode : str or bool
            Can be either 'x', 'y', 'closest' or False.
            Toggles how a tooltip appears on cursor hover.
        annotations : list
            Plotly annotations list.
        shapes : list or
            Plotly shapes list.
        title : string
            Chart title.
        dimensions : tuple
            Dimensions 2-tuple in order (width, height). Disables autosize=True.
        width : int
            Width of chart. Disables autosize=True.
        height : int
            Height of chart. Disables autosize=True.
        margin : dict or tuple
            Plotly margin dict or 4-tuple in order (l, r, b, t) or
            5-tuple in order (l, r, b, t, margin). Tuple input added for
            Cufflinks compatibility.

    """
    for key in layout:
        if key not in _VALID_LAYOUT:
            raise Exception("Invalid keyword '{0}'".format(key))

    # No utility right now, planned in the future for additions
    def _expand(base_layout):
        pass

    _expand(base_layout)

    # Modifiers directly to base_layout
    utils.update(base_layout, layout)

    legend = True  # Debug
    if legend:
        base_layout['showlegend'] = True
        if not isinstance(legend, bool):  # If not bool
            base_layout['legend'] = legend

    if hovermode:
        base_layout['hovermode'] = hovermode

    if annotations:
        base_layout['annotations'] = annotations

    if shapes:
        base_layout['shapes'] = shapes

    if title:
        base_layout['title'] = title

    if dimensions or height or width:
        base_layout['autosize'] = False

    if dimensions:
        base_layout['width'] = dimensions[0]
        bsae_layout['height'] = dimensions[1]

    if height:
        base_layout['height'] = height

    if width:
        base_layout['width'] = width

    if margin:
        base_layout['margin'] = margin

    # Custom layout update
    if custom_layout:
        layout = utils.update(layout, custom_layout)

    for key in base_layout:
        if key not in _VALID_LAYOUT:
            raise Exception("Invalid keyword '{0}'".format(key))

    return base_layout


def get_template(theme=None, layout=None,
                 legend=None, hovermode=None,
                 annotations=None, shapes=None, title=None,
                 dimensions=None, width=None, height=None, margin=None,
                 **kwargs):
    """Generate color, traces, additions and layout dicts.

    Parameters
    ----------
        theme : string
            Quantmod theme.
        layout : dict or Layout
            Plotly layout dict or graph_objs.Layout object.
            Will override all other arguments if conflicting as
            user-inputted layout is updated last.
        legend : dict, Legend or bool
            True/False or Plotly legend dict / graph_objs.Legend object.
            If legend is a bool, Quantmod will simply toggle legend visibility.
        hovermode : str or bool
            Can be either 'x', 'y', 'closest' or False.
            Toggles how a tooltip appears on cursor hover.
        annotations : list or Annotations
            Plotly annotations list or graph_objs.Annotations object.
        shapes : list or Shapes
            Plotly shapes list or graph_objs.Shapes object.
        title : string
            Chart title.
        dimensions : tuple
            Dimensions 2-tuple in order (width, height). Disables autosize=True.
        width : int
            Width of chart. Disables autosize=True.
        height : int
            Height of chart. Disables autosize=True.
        margin : dict or tuple
            Plotly margin dict or 4-tuple in order (l, r, b, t) or
            5-tuple in order (l, r, b, t, margin). Tuple input added for
            Cufflinks compatibility.

    """
    # Check for kwargs integrity
    if kwargs:
        for key in kwargs:
            if key not in _VALID_TEMPLATE_KWARGS:
                raise Exception("Invalid keyword '{0}'.".format(key))

    # Get skeleton
    skeleton = get_skeleton()

    # Test if theme is str or dict, or get default theme from config otherwise
    if theme:
        if instance(theme, six.string_types):
            theme = get_theme(theme)
        elif isinstance(theme, dict):
            pass
        else:
            raise Exception("Invalid theme '{0}'.".format(theme))
    else:
        theme = get_theme(auth.get_config_file()['theme'])

    # Test if layout is dict, else coerce Layout() to regular dict
    # Rename to custom_layout (to distinguish from base_layout and layout)
    if layout:
        custom_layout = layout
        if not isinstance(custom_layout, dict):
            try:
                custom_layout = dict(custom_layout.items())
            except:
                raise Exception("Invalid layout '{0}'.".format(custom_layout))
    else:
        custom_layout = None

    # Test if legend is True/False, else coerce Legend() to regular dict
    # if legend is not regular dict
    if legend:
        if isinstance(legend, bool):
            pass
        elif isinstance(legend, dict):
            pass
        else:
            try:
                layout = dict(layout.items())
            except:
                raise Exception("Invalid legend '{0}'.".format(layout))

    # Test if hovermode is str else raise exception (can also be False)
    if hovermode or hovermode == False:
        if not isinstance(hovermode, six.string_types):
            raise Exception("Invalid hovermode '{0}'.".format(hovermode))

    # Test if annotations is list, else coerce Annotations() to regular list
    if annotations:
        if not isinstance(annotations, list):
            try:
                annotations = list(annotations)
            except:
                raise Exception(
                    "Invalid annotations '{0}'.".format(annotations))

    # Test is shapes is list, else coerce Shapes() into regular list
    if shapes:
        if not isinstance(shapes, list):
            try:
                shapes = list(shapes)
            except:
                raise Exception("Invalid shapes '{0}'.".format(shapes))

    # Test below items if string, else raise exception
    if title:
        if not isinstance(title, six.string_types):
            raise Exception("Invalid title '{0}'.".format(title))

    # Test below items is tuple, else raise exception
    if 'figsize' in kwargs:  # Matplotlib
        figsize = kwargs['figsize']
        if isinstance(figsize, tuple) and len(figsize) == 2:
            dimensions = tuple(80 * i for i in figsize)  # 80x Matplotlib sizes
        else:
            raise Exception("Invalid figsize '{0}'.".format(figsize))
    elif dimensions:  # Cufflinks
        if not isinstance(dimensions, tuple) or len(dimensions) == 2:
            raise Exception("Invalid dimensions '{0}'.".format(dimensions))
    else:
        pass

    # Test below items if int, else raise exception
    if width:
        if not isinstance(width, six.integer_types):
            raise Exception("Invalid width '{0}'.".format(width))

    if height:
        if not isinstance(height, six.integer_types):
            raise Exception("Invalid height '{0}'.".format(height))

    # Test if margin is dict, else convert tuple to dict, else raise exception
    if margin:
        if isinstance(margin, dict):
            pass
        elif isinstance(margin, tuple):  # Cufflinks
            if len(margin) == 4:
                margin = dict(zip(('l', 'r', 'b', 't'), margin))
            elif len(margin) == 5:
                margin = dict(zip(('l', 'r', 'b', 't', 'pad'), margin))
            else:
                raise Exception("Invalid margin '{0}'.".format(margin))
        else:
            raise Exception("Invalid margin '{0}'.".format(margin))

    # Split theme and skeleton
    if all(key in skeleton for key in _VALID_BASE_COMPONENTS):
        base_colors = skeleton['base_colors']
        base_traces = skeleton['base_traces']
        base_additions = skeleton['base_additions']
        base_layout = skeleton['base_layout']
    else:
        raise Exception("Improperly configured skeleton. "
                        "Consider reinstalling Quantmod.")

    if all(key in theme for key in _VALID_THEME_COMPONENTS):
        colors = theme['colors']
        traces = theme['traces']
        additions = theme['additions']
        layout = theme['layout']
    else:
        raise Exception("Improperly configured theme '{0}'.".format(theme))

    # Generate final template
    final_colors = make_colors(base_colors, colors)
    final_traces = make_traces(base_traces, traces)
    final_additions = make_additions(base_additions, additions)
    final_layout = make_layout(base_layout, layout, custom_layout,
                               legend, hovermode,
                               annotations, shapes, title,
                               dimensions, width, height, margin, **kwargs)

    # Convert to dict
    template = dict(colors=final_colors, traces=final_traces,
                    additions=final_additions, layout=final_layout)

    return template


def get_base_layout(figures):
    """Generate a layout with the union of multiple figures' layouts.

    Parameters
    ----------
        figures : list
            List of Plotly figures

    """
    layout = {}
    for figure in figures:
        for key, value in figure['layout'].items():
            layout[key] = value
    return layout


def strip_figure(figure):
    """Strip a Plotly figure into multiple figures with a trace on each of them.

    Parameters
    ----------
        figure : dict or Figure
            Plotly figure

    """
    figures = []
    for trace in figure['data']:
        figures.append(dict(data=[trace], layout=figure['layout']))
    return figures
