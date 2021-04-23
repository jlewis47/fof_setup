import numpy as np
import os
from shutil import copyfile as cp



def read_file(tgt):

    lines=[]
    with open(tgt,'r') as src:
    
        for line in src:
            
            lines.append(line)

    return(lines)

def write_file(tgt,lines):
    
    with open(tgt,'w') as dest:
    
        for line in lines:
            
            dest.write(line)

    return(0)

def replace_key(lines,old_key,new_key):
    
    for line_nb,line in enumerate(lines):
        
        if old_key in line:
            
            lines[line_nb]=line.replace(old_key,new_key)

    return(lines)



fof_src_path='/linkhome/rech/genoba01/uoj51ok/fof_setup'


#read in source stuff

slurm_file=read_file(os.path.join(fof_src_path,'run_fof.slurm'))
in_file=read_file(os.path.join(fof_src_path,'fof.in'))
exec_file=os.path.join(fof_src_path,'fof_1024')


simpath='/gpfsscratch/rech/xpu/uoj51ok/1024/16Mpc/Metals_He_YDdust_BPASSV221_fesc0.5_Tsf3e4K_eps0.04_dtmmax0.5/'

cwd=os.getcwd()

#find outputs

dir_detections=os.listdir(simpath)
outputs=np.asarray([folder for folder in dir_detections if 'output' in folder])
output_paths=np.asarray([os.path.join(simpath,output) for output in outputs])


#for every output
for out_nb,output_path in enumerate(output_paths):

    out_name=outputs[out_nb]
    
    tgt_fof_dir=os.path.join(output_path,'fofs')

    if not os.path.isdir(os.path.join(tgt_fof_dir,'halos')):
        os.makedirs(os.path.join(tgt_fof_dir,'halos'))

        
    #executable
    exec_tgt=os.path.join(tgt_fof_dir,'fof_1024')
    if not os.path.isfile(exec_tgt):
        cp(exec_file,exec_tgt)
    os.chmod(exec_tgt,7777)
    
    #slurm
    loc_slurm_file=np.copy(slurm_file)
    loc_slurm_file=replace_key(loc_slurm_file,"name=fof","name=fof_%s"%out_name)
    loc_slurm_file=replace_key(loc_slurm_file,"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",tgt_fof_dir)

    write_file(os.path.join(tgt_fof_dir,'run_fof.slurm'),loc_slurm_file)

    #create .in file


    loc_in_file=np.copy(in_file)
    loc_in_file=replace_key(loc_in_file,'00019',out_name[-5:])
    write_file(os.path.join(tgt_fof_dir,'fof.in'),loc_in_file)    

    os.chdir(tgt_fof_dir)
    
    cmd_run="sbatch run_fof.slurm"
    os.system(cmd_run)



#return to initial working directory    
os.system('cd %s'%cwd)
