Abstract

This work is an attempt at training a model to automate the annotation of vocal/non-vocal regions of Arab-Andalusian music recordings. A large part of this work was devoted to feature extraction and dataset creation. At the moment, only spectral features are used for training, namely mel-frequency ceptral coefficients (MFCCs). However, it yet remains to incorporate temporal MFCC features from derivatives and spectral flux values. Artificial Neural Networks (ANNs) are used for this task. The dataset that was created consists of 4 recordings from the Arab Andalusian Corpus on Dunya, totaling of 190 minutes approximately, and with the audio sections of each annotated as either vocal/instrumental. Evaluation scores obtained by using mir_eval evaluation framework


Instructions

Download Audio files:
1. Download audio files from the following google drive, and copy the folder 'audio' into the cloned directory


Running the notebooks:
1. The notebook kernel used is python 3.
2. Several third party python packages are used, please find them in the first cell of either notebook and install them using pip. The only exception to this is essentia, where it is best to conslult the installation instructions on the website and download it as indicated for your chosen platform. https://essentia.upf.edu/documentation/installing.html
3. Step 1) notebook implements the feature extraction for the dataset used for train/test, and for another example test file used in Step 2) notebook
4. Step 2) involves training and testing the Artifical Neural Network. 




