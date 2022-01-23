from cgi import test
from glob import glob
from logging import captureWarnings
from re import sub
from time import sleep
import pandas as pd
from xml.etree import ElementTree as ET
import argparse, os
import subprocess
import sys
from session import Session
import random

def _makeFiles(path, path_to_video_file):
    
    ses = Session(path)
    t = ses.track['REF (Stereo)']
    df = t.data
    times = df[['start_time','end_time']]
    
    if not os.path.isdir('./xml_folder'):
            os.mkdir('./xml_folder')
    
    for i in range(len(df)):
        start_time, end_time = times.loc[i].values
        
        xml = ET.parse('template.xml')
        xml_iter = list(xml.iter())
        
        xml_iter[5].text = path_to_video_file
        xml_iter[6].text = str(start_time)
        xml_iter[7].text = str(start_time)
        xml_iter[8].text = str(end_time)
        
        xml = xml.getroot()
        
        s = (ET.tostring(xml, encoding='unicode', method='xml'))
        s = """<?xml version="1.0" encoding="utf-8"?>\n""" + s
        
        with open(f'./xml_folder/{i+1}.xml', 'w') as f:
            f.write(s)
        

        
def _singleConvert(in_path,out_path):
    """uses subprocess to spawn a subprocess which executes the dolby cmdline conversion tool

    Args:
        in_path (str): where to find the input xml
        out_path (str): where to drop the file after its created 
        
        return (subprocess): returns a subprocess instance which we can use to check that everything is complete 
    """
    args = ['/Applications/Dolby/Dolby Atmos Conversion Tool/cmdline_atmos_conversion_tool',
            '--pm_in', in_path,'--output_path', out_path,'--output_format', 'wav']
    # s = subprocess.run(args, capture_output=True)
    s = subprocess.Popen(['sleep', str(random.randint(1,8))], stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    return s


  
def _progress(a,b):
    sys.stdout.write('\r')
    p_a, p_b = (a/b)*30, (1-(a/b))*30
    p_ai = int(p_a)
    p_bi = int(p_b) + 1
    
    sys.stdout.write('*'*p_ai+ '-' * p_bi)  
    sys.stdout.flush()
    
    
    
def _convert_all(xml_file_path):
    paths = glob(f'{xml_file_path}/*.xml') #grab the paths to all the xmls in the file 
    subprocess = []
    for path in paths:
        print("hello")
        idx = os.path.split(path)[-1][:-4] # grab number
        
        sub = _singleConvert(path,f'Track{idx}') #launch subroutine 
        subprocess.append(sub) #track subroutines
    
    l = len(paths)
    while True:
        print("loo")
        failure = []
        success = []
        # for process in subprocess:
        #     print(process.stderr.read(),'poll')
        #     if process.poll() == 0:
        #         success.append(process)
        #     elif process.stderr.read() != b'':
        #         failure.append(process)
        
        num_done = len(failure) + len(success)
        _progress(num_done, l)
        if num_done == l:
            print("")
            print(f'conversions complete, num success: {len(success)}, num failure: {len(failure)}')
            return
        sleep(.1)
        
    
def FullConvert(path, path_to_video):
    
    _makeFiles(path,path_to_video)
    _convert_all('./xml_folder')
    os.rmdir('./xml_folder')
    
    
def main():
    print(__name__)
    # parser = argparse.ArgumentParser(description="args")
    # parser.add_argument("--xlsx", type=str, required=True)
    # parser.add_argument("--video_path", type=str, required=True)
    # args = parser.parse_args()
    _convert_all('./xml_folder')
    # test_convert()
    
    
def test_convert():
    _convert_all('./xml_folder')
    
def test_single_convert():
    _singleConvert('./xml_folder/dolby_0.xml','./test/convert.wav')
    
def xml_file_test():
    _makeFiles('./text.txt','text_curr')


if __name__ == '__main__':
    main()
print(__name__)