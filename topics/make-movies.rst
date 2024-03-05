.. _making-movies:

Making movies of your BFE field quantities
==========================================

Read in config from EXP yaml file and render a movie from the
coefficient file. This notebook will create the movie for either the
disk or the halo by changing the component variable from ‘dark’ to
‘star’ and vice versa.

Begin with the usual imports
----------------------------

You may need to append the pyEXP location to your Python path, depending
on your installation.

.. code:: python

    import os
    import copy
    import yaml
    # sys.path.append('/my/path/to/site-packages')
    import pyEXP
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import ticker, cm, colors
    from os.path import exists
    
    plt.rcParams['figure.figsize'] = [12, 9]

Configure the basis and component
---------------------------------

| At minimum, you need to - Define the EXP config file to import the
  config.
| - Define the target component.

The rest of the notebook should then run without changes.

Two optional parameters: - The half size of each axis - Number of pixels
along each axis

.. code:: python

    # key parameters
    exp_config = 'step3_try9.yml'
    component  = 'star'  # You can make the halo (disk) movie by changing this to 'dark' ('star')
    
    # options
    size       = 0.04
    npix       = 50

Switch to the working directory
-------------------------------

I like to be explicit about my working directory but you don’t need to
do this here. It would be sufficient to simply pass the full path to the
coefficient factory below or launch the notebook from a working
directory.

.. code:: python

    # os.chdir('/data/Nbody/Test')

Read the EXP config file, generate the basis from the config, and get the run tag for convenience
-------------------------------------------------------------------------------------------------

.. code:: python

    # Open and read the yaml file
    #
    with open(exp_config, 'r') as f:
        yaml_db = yaml.load(f, Loader=yaml.FullLoader)
        
    # Grab both star and dark, although I'm mostly interested in star at this point
    #
    for v in yaml_db['Components']:
        if v['name'] == component:
            config = yaml.dump(v['force'])
            
    # Construct the basis instance
    #
    basis = pyEXP.basis.Basis.factory(config)
    
    # Get the runtag
    #
    runtag = yaml_db['Global']['runtag']
    print("\nRuntag from {} is: {}".format(exp_config, runtag))
    coeffile = 'outcoef.{}.{}.h5'.format(component, runtag)
    print("\nCoef file is:", coeffile)

Read the coefficients
---------------------

.. code:: python

    coefs = pyEXP.coefs.Coefs.factory(coeffile)

Set the output field grid and render the slices
-----------------------------------------------

.. code:: python

    times = coefs.Times()
    pmin  = [-size, -size, 0.0]
    pmax  = [ size,  size, 0.0]
    grid  = [ npix,  npix,   0]
    
    fields = pyEXP.field.FieldGenerator(times, pmin, pmax, grid)
    
    print('Created fields instance')
    
    surfaces = fields.slices(basis, coefs)

Make a movie frames
-------------------

.. code:: python

    # Get the shape
    keys = list(surfaces.keys())
    nx = surfaces[keys[0]]['d'].shape[0]
    ny = surfaces[keys[0]]['d'].shape[1]
    
    # Make the mesh
    x = np.linspace(pmin[0], pmax[0], nx)
    y = np.linspace(pmin[1], pmax[1], ny)
    xv, yv = np.meshgrid(x, y)
    
    plt.rcParams.update({'font.size': 22})
    
    # Fix the contour levels to prevent jitter in the movie
    cbar1 = 10**np.arange(0.0, 4.01, 0.1)
    cbar2 = 10**np.arange(0.0, 4.01, 0.4)
    
    # Frame counter
    icnt = 0
    cmap = copy.copy(plt.colormaps['viridis'])
    
    N = cmap.N
    cmap.set_under(cmap(1))
    cmap.set_over(cmap(N-1))
    
    # Iterate through the keys
    for v in keys:
        fig, ax = plt.subplots(1, 1, figsize=(24, 20))
        
        mat = surfaces[v]['d']
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                if mat[i, j] < 1.0: mat[i, j] = 1.0
                if mat[i, j] > 10000.0: mat[i, j] = 10000.0
                
        cont1 = ax.contour(xv, yv, mat.transpose(), cbar2, colors='k')
        # You can label the contours inline by uncommenting the next two lines...
        # ax[0].clabel(cont1, fontsize=9, inline=True)
        # cont2 = ax.contourf(xv, yv, surfaces[v]['d'].transpose(), cbar2, vmin=cbar2[0], vmax=cbar2[-1])
        cont2 = ax.contourf(xv, yv, mat.transpose(), cbar1, locator=ticker.LogLocator())
        plt.colorbar(cont2, ax=ax)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('T={:4.3f}'.format(v))
        
        fig.savefig('{}_movie_{}_{:04d}.png'.format(component, runtag, icnt), dpi=75)
        plt.close()
    
        icnt += 1

Make a mp4 file from the frames using ffmpeg
--------------------------------------------

This only work if you have ‘ffmpeg’ installed, of course …

.. code:: python

    os.system('ffmpeg -y -i \'{0}_movie_{1}_%04d.png\' movie_{0}_{1}.mp4'.format(component, runtag))

Preview the new movie
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from IPython.display import Video
    Video('movie_{0}_{1}.mp4'.format(component, runtag), embed=True, width=800)
