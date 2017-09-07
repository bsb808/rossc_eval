import os
import logging
import subprocess
import glob

# Notebook
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from IPython.display import Image, display

def walk(path):
    fs = []
    ds = []
    for root, dirs, files in os.walk(path):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for directory in dirs:
            #paths.append(os.path.join(root, directory))
            ds.append(directory)
        for filename in files: 
            relDir = os.path.relpath(root,path)
            relFile = os.path.join(relDir,filename)
            #paths.append(os.path.join(root,filename))
            fs.append(relFile)
    return (ds,fs)

def callCmd(cmd):
    logging.info("Calling <%s>"%cmd)
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
    (output,err)=p.communicate()
    if output is not None:
        logging.info("stdout: %s"%output)
    if err is not None:
        logging.error("stderr: %s"%err)

def testTextStrings(fname,teststrs):
    '''
    Given the filename and a list of strings, seach the file to see if ALL
    the strings are present on a given line
    '''
    logging.info("Testing file <%s> for the occurance of all of the following strings on a single line:"%fname)
    logging.info("\t"+str(teststrs))
    try:
        f = open(fname)
    except IOError:
        logging.error("Can't open file!")
        return False
    result = False
    for line in f:
        tests = []
        for t in teststrs:
            tests.append(t in line)
        if all(tests):
            result = True
    logging.info("Result of search - %s"%str(result))
    return result 

def catFile(fpath):
    # Contents of file to logger
    logging.info("Contents of <%s>"%fpath)
    if not os.path.isfile(fpath):
        logging.error("File does not exist!")
    else:
        cmd = "cat %s"%fpath
        callCmd(cmd)
    return

def catFiles(repo,fpaths):
    for fpath in fpaths:
        catFile(os.path.join(repo,fpath))

def checkFiles(repo,flist):
    logging.info("Checking existence of files/directories...") 
    yes = 0
    no = 0
    for p in flist:
        path = os.path.join(repo,p)
        test = os.path.exists(path)
        logging.info("Does %s exist? %s"%(os.path.join(path),str(test)))
        if test:
            yes+=1
        else:
            no+=1
    if (no > 0 ):
        logging.warn("Only %d of %d files/directories exist"%(yes,yes+no))
    else:
        logging.info("Success: All %d of %d files/directories exist"%(yes,yes+no))
    return (yes,no)

def checkAllFiles(repo,flist):
    allthere = True
    logging.info("Checking for %d files"%len(flist))
    for f,ii in zip(flist,range(len(flist))):
        test = checkFile(repo,f)
        if test:
            logging.info("%d: Success",ii)
        else:
            logging.error("%d: Missing",ii)
            allthere = False
    return allthere

def checkFile(repo,f):
    path = os.path.join(repo,f)
    test = os.path.isfile(path)
    logging.info("Is there a file <%s>? %s"%(path,str(test)))
    return test

def checkDir(repo,d):
    path = os.path.join(repo,d)
    test = os.path.isdir(path)
    logging.info("Is there a directory <%s>? %s"%(path,str(test)))
    return test
                 
    
    

def dispImage(repo,fname):
    path=os.path.join(repo,fname)
    logging.info("Display image file <%s>"%path) 
    if not os.path.exists(path):
        logging.error("<%s> does not exist!"%path)
    else:
        display(Image(filename=path))

def dispImageList(repo,flist):
    for ff in flist:
        dispImage(repo,ff)

def images2pdf(repo,ilist,outpdf):
    logging.info("Attempting to assemble a PDF from the following list of images")
    logging.info(str(ilist))
    if len(ilist) == 0:
        logging.error("List appears empty!")
        return
    tmpdir = os.path.join(repo,'tmp')
    tmpdir = '/home/bsb/tmp'
    tmpdir = './tmp'
    if not os.path.isdir(tmpdir):
        os.mkdir(tmpdir)
    # make sure it is empty
    tlist = glob.glob(os.path.join(tmpdir,"*.*"))
    for f in tlist:
        os.remove(f)
    
    # Store all the rare file names
    tmpfiles = []

    for i in ilist:
        # full filename
        path = os.path.join(repo,i)

        # create output file name
        base = os.path.basename(i)
        nm,ext = os.path.splitext(base)


        # Does the file exist?
        test = os.path.isfile(path)
        logging.info("Does %s exist? %s"%(path,str(test)))
        if test:
            ifile = path
            caption = i
            ofile = os.path.join(tmpdir,"%s_rare%s"%(nm,ext))

            # If it is an SVG, convert to PNG
            if "svg" in ext.lower():
                # Convert to png
                pngf = os.path.join(tmpdir,"%s.png"%nm)
                logging.info("Use inkscape to convert <%s> to <%s>"%(path,pngf))
                cmd="inkscape -z -f %s -w 720 -e %s"%(path,pngf)
                logging.info("CMD: %s"%cmd)
                p = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
                (output,err)=p.communicate()
                if output is not None:
                    logging.info("stdout: %s"%output)
                if err is not None:
                    logging.error("stderr: %s"%err)
                    i = pngf
                path = os.path.join(repo,i)
                ifile = path
                ofile = os.path.join(tmpdir,"%s_rare.png"%(nm))
                

        else:
            ifile = 'missing.png'
            caption = i
            ofile = os.path.join(tmpdir,"%s_rare%s"%(nm,'.png'))
            
        cmd = 'bash add_caption.sh %s %s "%s"'%(ifile,ofile,caption)
        tmpfiles.append(ofile)
        logging.info("CMD: %s"%cmd)
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
        (output,err)=p.communicate()
        if output is not None:
            logging.info("stdout: %s"%output)
        if err is not None:
            logging.error("stderr: %s"%err)

    # Now put all images togeter into a pdf
    cmd = 'convert '
    for t in tmpfiles:
        cmd = cmd + t + " "
    cmd = cmd + " " + outpdf
    logging.info("CMD: %s"%cmd)
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
    (output,err)=p.communicate()
    if output is not None:
        logging.info("stdout: %s"%output)
    if err is not None:
        logging.error("stderr: %s"%err)
    

