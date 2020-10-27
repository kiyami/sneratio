## Package Name: SNeRatio

> **Definition:** A supernova ratio calculator for x-ray observation of galaxies and galaxy clusters.

> This package calculates the best fit percentage contribution of supernova types (SNIa and SNcc) for a given abundace data for selected yield tables and models.

> This package is introduced and used in the paper "The Relative Supernovae Contribution to the Chemical Enrichment History of Abell 1837". (Not published yet)


#### Installation:

> Type the following commands in terminal:
>
    $ git clone https://github.com/kiyami/sneratio.git
    $ pip3 install ./sneratio

> (Alternative way)
>
    $ git clone https://github.com/kiyami/sneratio.git
    $ cd sneratio
    $ python3 setup.py install

> After installation, you can remove the downloaded sneratio folder.


#### Usage:

> Type the following commands in python3 interactive shell
>
    >>> import sneratio
    >>> sneratio.run_app()

> Click "Load" button to load the test data.
>
> You can also load your data from a txt file by entering full path of the file and click "Load". 
> An example txt file is shown below:
>
    Element Abund AbundError
    Mg 0.190754 0.162
    Si 0.465456 0.106
    S 0.307239 0.1525
    Fe 0.515208 0.0265
    Ni 0.844307 0.349

> Make your selections and click "Fit".

> Save directory will be your current directory. (The current directory of the terminal that you initialized SNeRatio.)

> Feel free to make contributions or report bugs.
>
> M.K.Erdim


#### GUI:

![GitHub Logo](/examples/gui.png)


