import numpy as np
import argparse
import os
import time
from subprocess import call, check_output, STDOUT


def fun_kmc_fa(filename, dirpath, newfilename, tmpdir):
    
    print(time.asctime(time.localtime(time.time())))
    print("[KMC]:   running\n")
    file=newfilename.split('/')[-1]
    newfile=os.path.join(dirpath, file+".txt")
    
    
    kmcStd=check_output(["kmc", "-k21", "-fm", "@{}".format(filename), newfilename, tmpdir], stderr=STDOUT, universal_newlines=True)
    call(["kmc_tools", "transform", newfilename, "sort", ".", "dump", "-s", newfile], stderr=open(os.devnull, "w"))
    os.remove(newfilename+".kmc_pre")
    os.remove(newfilename+".kmc_suf")
    
    print(time.asctime(time.localtime(time.time())))
    print("[KMC]:   finished\n")
    


def fun_kmc_fq(filename, dirpath, newfilename, tmpdir):
    
    print(time.asctime(time.localtime(time.time())))
    print("[KMC]:   running\n")
    file=newfilename.split('/')[-1]
    newfile=os.path.join(dirpath, file+".txt")
    
    
    kmcStd=check_output(["kmc", "-k21", "@{}".format(filename), newfilename, tmpdir], stderr=STDOUT, universal_newlines=True)
    kmcArr=kmcStd.split('\n')
    call(["kmc_tools", "transform", newfilename, "sort", ".", "dump", "-s", newfile], stderr=open(os.devnull, "w"))
    os.remove(newfilename+".kmc_pre")
    os.remove(newfilename+".kmc_suf")
    
    print(time.asctime(time.localtime(time.time())))
    print("[KMC]:   finished\n")




def printUsage():
    print("python kmc.py [option] [option] [option]\n")
    print("Usage:\n")
    print("-f <str>     --file     fasta or fastq, If you have multiple fastq files, please Enter the files one after the other, separated by spaces\n")
    print("-d  <str>    --dirpath  the destination folder.\n")
    print("-t  <int>    --thread   total number of threads (default: 10)\n")
            
    

if __name__ == "__main__":
    
    
    parser=argparse.ArgumentParser("python kmc.py")
    parser.add_argument("--file", "-f", nargs="+", type=str, help="the genome fasta or the genome fastq, If you have multiple fastq files, please Enter the files one after the other, separated by spaces")
    parser.add_argument("--dirpath", "-d", type=str, help="the destination folder.")
    parser.add_argument("--thread", "-t", default=10, type=str, help="total number of threads (default: 10)")


    args=parser.parse_args()
    
    
    filenameDict=dict()
    newfilelist=[]
    
    print(time.asctime(time.localtime(time.time())))
    print("[START]:   start\n")
    try:
        
        if os.path.exists(args.dirpath) == False:
            os.makedirs(args.dirpath, exist_ok=True)
        
        # 相对路径转绝对路径
        if args.dirpath == '.':
            args.dirpath=os.getcwd()
        if args.dirpath[0] == '.' and args.dirpath[1] == '/':
            args.dirpath=os.path.join(os.getcwd(), args.dirpath[2:])
            
        # 读文件
        for file in args.file:
            if os.path.exists(file) == False:
                print("[ERROR]: The file {} is incorrect! ! !".format(file))
                break
            suftmp=file.split('/')[-1]
            # 提取文件名
            
            
            tmp_list = suftmp.split('.')[0].split('_')[0:len(suftmp.split('.')[0].split('_'))-1]
            filename="_".join(tmp_list)
            print(filename)

            
            newfilename=os.path.join(args.dirpath, filename)
            newfile=os.path.join(args.dirpath, filename+".lst")
            newfilelist.append(newfile)
            type = suftmp.split('.')[-1]

            #avg_length, max_length, total_length, n_reads=sequence_stat(file, str(args.thread))
            with open(newfile, "a+") as f:
                f.write("{}\n".format(file))
            filenameDict[newfilename]=newfile
    
        try:
            if suftmp.endswith('fasta') or suftmp.endswith('fa') or suftmp.endswith('fasta.gz') or suftmp.endswith('fa.gz'):
                for key, value in filenameDict.items():
                    fun_kmc_fa(value, args.dirpath, key, args.dirpath)
            if suftmp.endswith('fastq') or suftmp.endswith('fq') or suftmp.endswith('fastq.gz') or suftmp.endswith('fq.gz'):
                for key, value in filenameDict.items():
                    fun_kmc_fq(value, args.dirpath, key, args.dirpath)
        except Exception as e:
            print("[ERROR]: ", e)
        
        
        for file in newfilelist:
            if os.path.exists(file):
                os.remove(file)
        
        print(time.asctime(time.localtime(time.time())))
        print("[END]:   END\n")
    except Exception as e:
        print(time.asctime(time.localtime(time.time())))
        print("[ERROR]: ", e)
        #print("\n[ERROR TYPE]: 'NoneType' object is not iterable\n[CAUSE]: No file has been provided.")
        #print("\n[ERROR TYPE]: expected str, bytes or os.PathLike object, not NoneType.\n[CAUSE]: The file input is incorrect or the dirpath is incorrect.")    
        print()
        printUsage()
            
