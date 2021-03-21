import matplotlib.pyplot
import os

def plot(x, y, figureTitle=None,
               figureSize=[8, 6],
               title=None,
               xlabel=None,
               ylabel=None,
               xlim=None,
               ylim=None,
               xgrid=False,
               ygrid=False,
               tickLabelSize='x-small',
               label=None,
               widthScale=0.8,
               color=['r', 'g', 'b', 'c', 'm', 'y'],
               marker=[' ', ' ', ' ', ' ', ' ', ' '],
               linestyle=['-', '-', '-', '-', '-', '-'],
               linewidth=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
               xvLine=None,
               xvLinestyle=':',
               xvLinecolor='k',
               display=True,
               saveFilename=None,
               closeFigure=False):
   """
   title::
      plot

   description::
      This method will plot the two-dimensional data set(s) provided and 
      optionally display them to the screen or save them to a output 
      graphics format file.  This method serves as a wrapper for the
      Matplotlib module incorporating and simplifying the use of the 
      more commonly available graphing option.

   attributes::
      x
         A 1-dimensional list-like object or list of list-like objects
         containing the independent (abscissa) data for the plot to be
         created.
      y
         A 1-dimensional list-like object or list of list-like objects
         containing the dependent (ordinate) data for the plot to be
         created.
      figureTitle
         A string containing the title to be displayed in the window bar
         of a plot created for display on the screen. [default is None]
      figureSize
         A list or tuple containing the size, in inches, for the created
         plot. [default is [8, 6]]
      title
         A string containing the title to be displayed on the plot.
         [default is None]
      xlabel
         A string containing the label for the independent/abscissa/
         horizontal axis. [default is None]
      ylabel
         A string containing the label for the dependent/ordinate/
         vertical axis. [default is None]
      xlim
         A list or tuple containing the minimum and maximum values for
         the independent/abscissa/horizontal axis. [default is None which
         implies that autoscaling will be used]
      ylim
         A list or tuple containing the minimum and maximum values for
         the dependent/ordinate/vertical axis. [default is None which
         implies that autoscaling will be used]
      xgrid
         A boolean indicating whether vertical grid lines should be 
         displayed in the plot field. [default is False]
      ygrid
         A boolean indicating whether horizontal grid lines should be 
         displayed in the plot field. [default is False]
      tickLabelSize
         A string indicating the size of the font to be used for the
         tick labels on both axes. Valid values for this attribute are
         'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 
         'xx-large', 'larger', and 'smaller'. [default is 'x-small']
      label
         A list of strings containing the labels to be used in the legend, 
         one for each data set provided.  If there is to be no legend 
         label for a provided data set, insert None in the proper list 
         position. If no legend is to be displayed, provide a scalar 
         value of None for this attribute. [default is None]
      widthScale
         A scalar in the range 0.0 to 1.0 indicating the fraction to the 
         default axis width in the horizontal direction that this axis 
         should occupy when a legend is to be displayed. This attribute 
         is ignored when no label attributes are provided. [default is 0.8]
      color
         A list of strings describing a cyclical sequence of colors to be
         used for individual plot lines and symbols.  This sequence will
         repeat if more plots exist than colors in this list.  Any valid
         Matplotlib color is permissible. [default is ['r', 'g', 'b', 'c',
         'm', 'y']]
      marker
         A list of strings describing a cyclical sequence of plot markers 
         to be used for individual plot lines.  This sequence will repeat 
         if more plots exist than marker types in this list.  Any valid
         Matplotlib marker type is permissible. [default is [' ', ' ', 
         ' ', ' ', ' ', ' '], i.e. no marker symbols]
      linestyle
         A list of strings describing a cyclical sequence of line styles 
         to be used for individual plot lines.  This sequence will repeat 
         if more plots exist than line styles in this list.  Any valid
         Matplotlib line style is permissible. [default is ['-', '-', 
         '-', '-', '-', '-'], i.e. solid lines]
      linewidth
         A list of floats describing a cyclical sequence of line widths 
         to be used for individual plot lines.  This sequence will repeat 
         if more plots exist than line widths in this list.  Any valid
         positive floating point number is permissible. [default is [1.0, 
         1.0, 1.0, 1.0, 1.0, 1.0]]
      xvLine
         A scalar indicating the x-position, in data units, of a vertical
         line to be drawn on the plot. [default is None]
      xvLinestyle
         A string describing the line style to be used for the vertical
         line, if desired. [default is ':']
      xvLinecolor
         A string describing the line color to be used for the vertical
         line, if desired. [default is 'k']
      display
         A boolean indicating if the created plot should be diplayed to
         the screen. [default is True]
      saveFilename
         A string containing the filename to be used when saving the plot
         to a graphics format file.  The extension contained in the
         filename will be used to indicate the graphics format to be used
         when saving the file. Some valid extensions include 'pdf', 'eps',
         'png', 'tif', 'tiff', 'jpg', and 'jpeg'.  A value of None 
         indicates that no file is to be created. [default is None]
      closeFigure
         A boolean indicating if the created created figure should be closed
         upon completion of this method. [default is False]

   returns::
      None

   author::
      Carl Salvaggio

   copyright::
      Copyright (C) 2020, Rochester Institute of Technology

   license::
      GPL

   version::
      1.0.1

   disclaimer::
      This source code is provided "as is" and without warranties as to 
      performance or merchantability. The author and/or distributors of 
      this source code may have made statements about this source code. 
      Any such statements do not constitute warranties and shall not be 
      relied on by the user in deciding whether to use this source code.
      
      This source code is provided without any express or implied warranties 
      whatsoever. Because of the diversity of conditions and hardware under 
      which this source code may be used, no warranty of fitness for a 
      particular purpose is offered. The user is advised to test the source 
      code thoroughly before relying on it. The user must assume the entire 
      risk of using the source code.
   """

   # Make sure the same number of independent and dependent data sequences
   # are provided, if only one set is provided, make sure they contain the
   # same number of values
   if len(x) != len(y):
      msg = 'The size of the provided data set does not match'
      raise ValueError(msg)

   # If more than one data sequence is provided, make sure the length of
   # each set is the same, the number of labels for the legend matches the
   # number of data sequences, and if no labels are provided create an
   # empty set
   multipleDatasets = hasattr(x[0], '__iter__')
   if multipleDatasets:
      for i in range(len(x)):
         if len(x[i]) != len(y[i]):
            msg = 'The size of the provided data sets do not match'
            raise ValueError(msg)
      if label:
         if len(label) != len(y):
            msg = 'The number of labels do not match the number of data sets'
            raise ValueError(msg)
      else:
         label = []
         for i in range(len(y)):
            label += [None]

   # Create a Matplotlib figure with the given title
   figure = matplotlib.pyplot.figure(figureTitle)

   # Turn off warnings for too many figures open
   matplotlib.pyplot.rcParams.update({'figure.max_open_warning': 0})

   # Set the figure size
   figure.set_size_inches(figureSize[0], figureSize[1])

   # Add a single sub plot to the figure
   axes = figure.add_subplot(1, 1, 1)

   # Set the values for those plot parameters that have been specified
   if title:
      axes.set_title(title)
   if xlabel:
      axes.set_xlabel(xlabel)
   if ylabel:
      axes.set_ylabel(ylabel)
   if xlim:
      axes.set_xlim(xlim)
   if ylim:
      axes.set_ylim(ylim)
   if xgrid:
      axes.xaxis.grid(True, linestyle=':', color='#e0e0e0')
   if ygrid:
      axes.yaxis.grid(True, linestyle=':', color='#e0e0e0')

   # Set the font size for the tick labels (relative to the default for
   # the backend being used)
   tickLabels = axes.get_xticklabels() + axes.get_yticklabels()
   for tickLabel in tickLabels:
      tickLabel.set_size(tickLabelSize)

   # Create the plot(s) for the provided data sequence(s)
   displayLegend = False
   if multipleDatasets:
      for i in range(len(x)):
         if label[i]:
            displayLegend = True
            axes.plot(x[i], y[i], label=label[i],
                                  linestyle=linestyle[i % len(linestyle)],
                                  linewidth=linewidth[i % len(linewidth)],
                                  marker=marker[i % len(marker)],
                                  color=color[i % len(color)])
         else:
            axes.plot(x[i], y[i], linestyle=linestyle[i % len(linestyle)],
                                  linewidth=linewidth[i % len(linewidth)],
                                  marker=marker[i % len(marker)],
                                  color=color[i % len(color)])
      if displayLegend:
         box = axes.get_position()
         axes.set_position([box.x0, box.y0, box.width*widthScale, box.height])
         legend = axes.legend(loc='center left', bbox_to_anchor=(1, 0.5))
   else:
      axes.plot(x, y, linestyle=linestyle[0], 
                      linewidth=linewidth[0], 
                      marker=marker[0], 
                      color=color[0])

   # If desired, draw a vertical line at the specified x location
   if xvLine:
      axes.axvline(x=xvLine, linestyle=xvLinestyle, color=xvLinecolor)

   # If desired, save the plot to an output graphics format file
   if saveFilename:
      basename, extension = os.path.splitext(saveFilename)
      saveFormat = extension[1:]
      if displayLegend:
         matplotlib.pyplot.savefig(saveFilename, format=saveFormat,
                                                 dpi=300,
                                                 bbox_extra_artists=(legend,),
                                                 bbox_inches='tight')
      else:
         matplotlib.pyplot.savefig(saveFilename, format=saveFormat,
                                                 dpi=300,
                                                 bbox_inches='tight')

   # If desired, display the plot to the screen
   if display:
      matplotlib.pyplot.show()

   if closeFigure:
      matplotlib.pyplot.close('all')


if __name__ == '__main__':
   import graphics
   import numpy
   import os

   x = []
   y = []
   label = []
   for i in range(6):
      x += [numpy.arange(11)]
      y += [(i + 1) * x[i]]
      label += ['$y = %ix$' % i]

   saveFilename = 'plot.pdf'

   graphics.plot(x[0], y[0])
   graphics.plot(x, y)
   graphics.plot(x, y, label=label, saveFilename=saveFilename)

