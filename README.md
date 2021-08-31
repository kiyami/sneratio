## SNeRatio: *A supernova ratio calculator for x-ray observation of galaxies and galaxy clusters.*

> **Note**
>
> * If you use this package either from the source code or from the web app for a publication please cite:
> 
>      *The Relative Supernovae Contribution to the Chemical Enrichment History of Abell 1837* (In review..)

> **Web App**
> 
> This package can be used as a web app from the following link:
> 
> https://sneratio.herokuapp.com/

> **Description** 
> 
> A supernova ratio calculator for x-ray observation of galaxies and galaxy clusters.
>
> Inter Cluster Medium (ICM) is the hot plasma that fills the environment in galaxy cluster.
> This plasma has been enriched in element abundance as a result of nucleosynthesis that takes place in stars and
> supernova explosions (SNe) over billions of years. Different types of SNe produce each element in different
> proportions. There are many studies on which SNe type will produce how much of each element, and it is available
> as "SNe yield tables" in the literature. Using elemental abundance measurements in plasma, it is possible to
> predict which type of SNe at what percentage. The same is true for the plasma that fills the interstellar
> environment within galaxies. The **SNeRatio** package makes this SNe ratio estimation using elemental abundance
> measurements. 
> 
> This package calculates the best fit percentage contribution of supernova types (SNIa and SNcc) for a given abundance
> data for selected yield tables and models.
>
> This package is introduced and used in the paper "The Relative Supernovae Contribution to the Chemical Enrichment
> History of Abell 1837". (In review..)


#### Usage:
* From Web App:
  > * Open https://sneratio.herokuapp.com/
  > * Select an __'SNIa Model'__ (yield table)
  > * Select an __'SNcc Model'__ (yield table)
  > * Select __'SNcc Mass Range'__ for integration with IMF function
  > * Select an __'IMF'__ (Initial Mass Function)
  > * Select a __'Solar Table'__
  > * Select a __'Reference Element'__. This selection turns your input abundace values into a ratio with
       reference element (e.g. X/Fe). 
  > * Select __'Confidence Interval'__ for uncertainty calculations.
  > * Data input:
  >     * Enter your values from 'Abundance Values' column;
  > 
  >         Click the little box next to the element name for activation, then enter the abundance
            value into the 'Value' box and uncertainty value into the 'Error' box.
  > 
  >     * Note: The reference element should be selected. At least 3 elements should be selected.
          Asymmetric uncertainties can not be used yet.
  >    
  > * Click __'Fit'__ button
  > 
  > 
  > After a few seconds, the fit plot should be visible in the middle panel, and the fit results will be shown below.
  > 

* Installing, and using locally:
    > 
    >   1- Type the following commands in terminal
    >
        $ git clone https://github.com/kiyami/sneratio.git
        $ pip3 install ./sneratio
        $ cd sneratio
        $ python3 app.py
    >
    >   2- Open the address shown in the terminal from the internet browser. 
    >    
    >   (http://127.0.0.1:5000/)
    > 
    >   3- Make your selections and click "Fit".
  
> Feel free to make contributions or report bugs.
>
> M.K.Erdim
> 
> mkiyami@yildiz.edu.tr
> 
> kiyamierdim@gmail.com
> 


#### GUI:

![GitHub Logo](/examples/gui.png)


<!-- >     * Load your abundance data via __'Browse'__ button;
>         
>         Prepare a text file that contains 3 columns with column names __"Element"__, __"Abund"__ and __"AbundErr"__
          written in the first row. The following rows should contain element name, abundance value and abundance
          uncertainty (e.g. __"Fe 0.78 0.01"__) -->