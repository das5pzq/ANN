BKM10 Formulism with pytorch tools

This is based on the BKM10 formulism for a sample of the real HallA data (data_hallA_allv2.csv) and also pseudo data that contain the truth value (pseudo_KM15.csv)  ,which proved can be extracted using local fit. 

There are 4 fit parameters which are 3 CFFs and a constant dvcs term. This code is based on PyTorch. To run the code run:

singularity run --nv /home/za2hd/pytorch-1.5.1.sif ann.py

First, you need to copy the pytorch*.sif file to your home directory. More information about container and singularity in Rivanna can be seen here: https://www.rc.virginia.edu/userinfo/rivanna/software/containers/ and https://www.rc.virginia.edu/userinfo/rivanna/software/pytorch/

The output is a series of number indicate: ReH, ReE, ReHTilde, final loss number, loss val 1, loss val 2 , loss val3. loss val 1,2 and 3 are validation loss that you can choose from the available functions or you can also create your own

The code also outputs plot of the fit for each dataset. For example

https://user-images.githubusercontent.com/68297438/145281206-1dff06ea-b2e2-482f-8ae1-fd7877b8162c.png

To run the job on grid ./jobscript.sh job_name replica_number. For example ./jobscript.sh CFF_BKM_Test 1000

If you use tensorflow, you need to modify the code. In BHDVCS_torch.py you need to change torch.cos to np.cos (just an example if you use numpy). I think you also need to modify the loss function (MSE, MAE, etc)

Email me if you have question: za2hd@virginia.edu
