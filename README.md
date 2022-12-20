## **SNeRatio**: *A supernova ratio calculator for x-ray observation of galaxies and galaxy clusters.*

> **Citation**
>
> If you use this package either from the source code or from the web app for a publication please cite:
> 
> *M K Erdim, C Ezer, O Ünver, F Hazar, M Hudaverdi, The relative supernovae contribution to the chemical enrichment history of Abell 1837, Monthly Notices of the Royal Astronomical Society, Volume 508, Issue 3, December 2021, Pages 3337–3344*
>
> https://doi.org/10.1093/mnras/stab2730

> **Web App (Under Maintenance)**
> 
> ~~This package can be used as a web app from the following link:~~
> 

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


#### **Usage**:
* Installing, and using locally:
    >   (Type the following commands in terminal)
    >
    >   1- Create a Python virtual environment (Optional)
    >
        $ cd /path/of/the/installation/   # go to the path that you want to install the app
        $ python3 -m venv venv            # create a python3 virtual environment named venv
        $ source venv/bin/activate        # activate the virtual environment
    > 
    >   2- Clone the repository and install the requirements.
    >
        (venv) $ git clone https://github.com/kiyami/sneratio.git   # clone the repository (or download from github.com)

        (venv) $ cd sneratio                                        # change directory
        (venv) $ pip3 install -r requirements.txt                   # install the required libraries via pip3
    >
    >   3- Prepare a data file for your abundance values as the example file 'test_data.txt' in 'data' folder.
    >
    >   4- Open the 'main.py' with a text editor and update the 'my_selections' part. 
    >   
    >   For example: 
    >
    >       "abund_data": "data/abund_data.txt" -> enter the path of your data file
    > 

    >   5- Run the app.
    >
        (venv) $ python3 main.py                                     # run the app
    > 

    >   6- Check the results from the 'outputs' folder.
    >

    >   7- Deactivate the virtual environment.
    > 
        (venv) $ deactivate

    >   8- To uninstall the app, delete the "sneratio" and "venv" folders.

> Feel free to make contributions or report bugs.
>
> M.K.Erdim
> 
> mkiyami@yildiz.edu.tr
> 
> kiyamierdim@gmail.com
> 
