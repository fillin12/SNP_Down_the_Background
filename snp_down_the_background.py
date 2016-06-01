######################
## .vcf SNP Sorter v1.2

######################
## Fixes: 
## 1) When not given an output name, the program faults.
## 2) Generate a .vcf instead of a .txt file so it can be manipulated further 

import os
import sys

arg_list = []

for arg in sys.argv:
    arg_list.append( arg )

if ( "--help" in arg_list ) or ( "-help" in arg_list ) or \
   ( "-h" in arg_list ) or ( "-H" in arg_list ) or ( "--H" in arg_list ) or \
   ( "--Help" in arg_list ) or ( "-Help" in arg_list ) or ( "--h" in arg_list ) :

    print( "\n\nSNP Down the Background", \
           "\n---------------------------------------------------------------------------", \
           "\n\tsnp_down_the_background.py is a program that will filter", \
           "\n\tSNPs from .vcf files if those SNPs are found in a", \
           "\n\treference and output the SNPS that are only found in the", \
           "\n\tnon-reference .vcf file.", \
           "\n\tTo use this program, the command should look like this:",\
           "\n\n\t$ python3 snp_down_the_background.py input_reference.vcf output_file.txt\n")
    quit()


try:
    vcf_reference_SNP_file_name = arg_list[1]
    output_file_name = arg_list[2]

except IndexError: #looks to see if you have the correct command
    print( "ERROR: The command you've entered was not correct.", \
           "\n\n\tThe line should look like this:", \
           "\n\tpython3 snp_down_the_background.py input_reference.vcf output_file.txt" )


try:   
    if vcf_reference_SNP_file_name[-4:] != ".vcf":
        print( "ERROR: The input file you have given is not a .vcf file." )
        quit()

    else:
        try:
            reference_file = open ( vcf_reference_SNP_file_name, "r" )

        except IOError:
            print( "That file does not appear to exist in your current directory. Try Again." )
            quit()
        
except NameError:
    quit()
    

if output_file_name[-4:] != ".txt": 
    output_file_name = output_file_name + ".txt" #Adds ".txt" to the end of the name


#########################
## Begin gathering the data from the file

reference_SNPs = []

num = 0

for lines in reference_file:
    
    if lines[0] != "C":
        continue

    num += 1
    split = lines.split()
    important_info = split[1], split[3], split[4]
    reference_SNPs.append( important_info )

SNP_Dict = {}
count = 0

file_list = os.listdir()
#print( file_list ) #Shows the contents of your directory

for file_names in file_list:

    if ( file_names[-4:] != ".vcf" ) or ( file_names == vcf_reference_SNP_file_name):
        #print( "Not a .vcf file" )
        continue
    
    
    file_object = open( file_names , "r" )

    SNP_list = []

    for lines in file_object:
        
        if lines[0] != "C":
            continue

        split_line = lines.split()
        important_info = split_line[1], split_line[3], split_line[4], True
        SNP_list.append( list( important_info ) )

    SNP_Dict[ file_names ] = SNP_list

    file_object.close()
    

num = 0
        
for mutant, SNP_list in SNP_Dict.items():

    for SNPs in SNP_list:

        num += 1
        
        for wt_snps in reference_SNPs:
        
            if (SNPs[0] == wt_snps[0]):

                SNPs[3] = False

    #print( "Mutant: ", mutant, num )
    num = 0
                
final_dict = {}

for mutants, SNP_list in SNP_Dict.items():

    final_dict[ mutants ] = []
    
    for SNPs in SNP_list:

        if SNPs[3]:

            final_dict[ mutants ].append( SNPs )

            
new_file = open( output_file_name , "w" ) # Begin writing ouutput file    

print( "Source file: <name_of_file> \nLocation    Original    Mutant", file = new_file )

for file_name, final_snp_list in final_dict.items():

    print( "\nSource file: ", file_name, file = new_file )

    for snps in final_snp_list:

        print ( snps[0], snps[1], snps[2], file = new_file )


new_file.close()









        

    
    
