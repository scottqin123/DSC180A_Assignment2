import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import subprocess as sp
import shlex
import os

def pca_first_round(fp = 'data/interim', fn, op):
	cmd = shlex.split('mkdir -p ' + fp)
	sp.call(cmd, shell = True)
	cmd = shlex.split('plink2   --vcf /datasets/dsc180a-wi20-public/Genome/vcf/sample/' + fn + '   --make-bed   --snps-only   --maf 0.05   --geno 0.1   --mind 0.05   --recode   --out data/interim/' + op)
	sp.call(cmd, shell = True)
	cmd = shlex.split('plink2 --bfile data/interim/' + op + ' --pca')
	sp.call(cmd, shell = True)

def remove_outlier(file):
	# read the vcf file as a dataframe
	tb = pd.read_table(file, header = None, sep = ' ')

    # calculate the standard deviation and multiply it by 2
	twostdv = np.std(tb[2])*2

    #reindex
	temp = tb.set_index(tb[0])
	temp = temp.drop([0,1], axis = 1)

    # choose the first 10 components
	temp = temp.iloc[:, 0:10]
    #select the outliers, which are two standard deviation away from the mean
	ol = (temp.abs()<twostdv).all(axis = 1)
	ollist = list(ol[ol == False].index)
    #write the outlier list into a text file
	with open('ollist.txt', 'w') as filehandle:
		for listitem in o:
			filehandle.write('%s\n' % listitem)

def first_plot(file):
	tb = pd.read_table(file, header = None, sep = ' ')
	tb.plot(2,3, kind = 'scatter')

def pca_second_round(op):
	cmd = shlex.split('plink2 --bfile data/interim/' + op + '--remove-fam listfile.txt --pca')
	sp.call(cmd, shell = True)

def second_plot(file):
	tb = pd.read_table(file, header = None, sep = ' ')
	tb.plot(2,3, kind = 'scatter')








#mkdir -p data/interim
#plink2   --vcf /datasets/dsc180a-wi20-public/Genome/vcf/sample/chr22_test.vcf.gz   --make-bed   --snps-only   --maf 0.05   --geno 0.1   --mind 0.05   --recode   --out data/interim/chr22
#plink2 --bfile data/interim/chr22 --pca
#plink2 --bfile data/interim/chr22 --remove-fam listfile.txt --pca
