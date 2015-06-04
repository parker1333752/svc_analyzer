import datetime, time
import subprocess
from config import AlgorithmFolder

class TxAlgorithm(object):

    def __init__(self, name):
        self.name = AlgorithmFolder+'/'+name
        self.description = ''
        self.createDate = datetime.datetime.now().time()
        self.inputsfilename=AlgorithmFolder+'/input.txt'
        self.outputsfilename=AlgorithmFolder+'/output.txt'

    def execute(self, inputs):
        #time.sleep(1)
        #return '(Algorithm: ' + self.name + ' execute ' + input + ')'

        f=open(self.inputsfilename,'w')
        for s in inputs:
            f.write(str(s)+'\n')
        f.close()

        fin=open(self.inputsfilename,'r')
        fout=open(self.outputsfilename,'w')
        fout.close()
        fout=open(self.outputsfilename,'w')
        if self.name[-2:]=='py':
            p=subprocess.Popen(['python',self.name],cwd=AlgorithmFolder)
        else:
            p=subprocess.Popen(self.name,cwd=AlgorithmFolder)

        # maybe use select-pool can optimize this wait
        returncode=p.wait()
        fin.close()
        fout.close()

        outputs=self.getOutputs()
        print '\talgorithm: (%s),\n\toutput = %r\n\treturncode = %d'%(self.name,outputs,returncode)
        return outputs

    def getOutputs(self):
        f=open(self.outputsfilename,'r')
        temp=f.readlines()
        for i in xrange(len(temp)):
            temp[i]=temp[i][:-1]
        f.close()
        return temp
