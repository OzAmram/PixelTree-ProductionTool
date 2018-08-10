import os
import subprocess as sp
import json

class TreeProduction(object):
  """
  Useful links:

  xrdcp root://eoscms//eos/cms/store/group/dpg_tracker_pixel/comm_pixel/PixelTree/2017/MC/PixelTree_MC_0.root .

  """
  def __init__(self):

    self.print_nice('status', '\n**** Welcome to TreeProduction ****')
                                       
    self.dataset          = '/RelValTTbarLepton_13/CMSSW_10_0_0_pre3-100X_mc2017_realistic_v1-v2/GEN-SIM-RECO'
    self.data_type        = 'collisions' #'cosmics'
    self.run_number       = ['1']
    self.CMSSW_version    = 'CMSSW_10_1_0_pre3'
    self.global_tag       = '101X_upgrade2018_realistic_Candidate_2018_03_15_16_26_46'
    self.SCRAM_ARCH       = 'slc6_amd64_gcc630'

    self.script_template  = 'MC_simhit' # 'reco' 'raw', 'cosmics', 'test', 'MC', 'MC_simhit'
    self.tree_production  = 'Pixel' # 'LA', 'Pixel'
    self.force_all        = False
    self.send_jobs        = True
    self.number_of_events = '10000'
    self.number_of_jobs   = 20
    self.batch            = 'lxbatch' # 'condor' # 

    self.postfix          = 'mc_evts' #'_gainPBPv6_715'

    self.path_working_dir = os.path.dirname(os.path.abspath(__file__))
    self.path_batch       = os.path.join(self.path_working_dir, 'batch')
    self.path_templates   = os.path.join(self.path_working_dir, 'templates')
    self.path_destination = {
      'Pixel' : '/store/group/dpg_tracker_pixel/comm_pixel/PixelTree/2017/' + self.data_type,
      'LA'    : ''
    }

    self.list_of_input_files = {}

    # When you call voms-proxy-init --voms cms --valid 168:00
    # As a result you get the output like /tmp/x509up_u78012
    # Then copy this x509up_u78012 wherever you want and this is voms_user_proxy
    self.voms_user_proxy  = '/afs/cern.ch/user/b/bmesic/x509up_u78012'

    self.print_nice('status', 'Dataset: {0}'.format(self.dataset))
    self.print_nice('status', 'Run number: {0}'.format(','.join(self.run_number)))
    self.print_nice('status', 'CMSSW version: {0}'.format(self.CMSSW_version))
    self.print_nice('status', 'global tag: {0}'.format(self.global_tag))
    self.print_nice('status', 'SCRAM_ARCH: {0}'.format(self.SCRAM_ARCH))    

    self.print_nice('status', '\nWorking directory: {0}'.format(self.path_working_dir))

  def get_list_of_input_files(self):
  
    self.print_nice('python_info', '\nCalled get_list_of_input_files function.')  

    for _r in self.run_number:

      _path_batch       = self.make_directory( os.path.join( self.path_batch, self.tree_production, _r + self.postfix))
      _path_output_file = os.path.join( self.path_batch, _r + '.txt')

      # If file does not exist or force redo call das_client
      if not os.path.exists(_path_output_file) or self.force_all:

        with open(_path_output_file, 'w') as _f:
          # _command = ['das_client', '--query="file run={0} dataset={1}"'.format( _r, self.dataset), '--limit=0']
          _command = ['/cvmfs/cms.cern.ch/common/das_client', '--query="file run={0} dataset={1}"'.format( _r, self.dataset), '--limit=0']
          # _command      = ['/cvmfs/cms.cern.ch/common/das_client', '--query="file dataset={0}"'.format(self.dataset), '--limit=0']
          print ' '.join(_command)
          _output  = sp.check_output(' '.join(_command), shell=True)
          _f.write(_output)

      else:
        self.print_nice('status', 'File already exists: {0}'.format(_path_output_file)) 

      with open(_path_output_file, 'r') as _f:
        self.list_of_input_files[_r] = _f.read().splitlines()
        # self.list_of_input_files = ['a']*self.number_of_jobs
  
  def make_directory_eos(self):

    self.print_nice('python_info', '\nCalled make_directory_eos function. Copy output of this function and run at EOS file') 

    for _r in self.run_number:
      print 'mkdir {0}{1}'.format(_r, self.postfix)

  def make_send_jobs(self):
    
    self.print_nice('python_info', '\nCalled make_send_jobs function.')  

    for _rr, _lf in self.list_of_input_files.iteritems():

      self.print_nice('status', '\nWorking on run: {0}'.format(_rr))

      _path_batch_dir = self.make_directory( os.path.join(self.path_batch, self.tree_production, _rr + self.postfix))

      for _i, _f in enumerate(_lf):

        if _i > self.number_of_jobs - 1 and self.number_of_jobs != -1:
          continue

        # ---------------
        # shell_template
        with open( os.path.join(self.path_templates, 'shell.sh'), 'r') as _shell_template_file:
          _shell_template = _shell_template_file.read()
    
        _replace_strings_shell = {
          '<SCRAM_ARCH>'                : self.SCRAM_ARCH,
          '<X509_USER_PROXY>'           : self.voms_user_proxy,
          '<working_directory>'         : self.path_working_dir,
          '<path_python_file>'          : os.path.join( _path_batch_dir, '_' + str(_i) + '.py'),
          '<root_file_name>'            : 'PixelTree_' + _rr + '_' + str(_i) + '.root',
          '<root_file_name_destination>': os.path.join( self.path_destination[self.tree_production], _rr + self.postfix) 
        }

        for _r, _rw in _replace_strings_shell.iteritems():
          _shell_template = _shell_template.replace(_r, _rw)

        with open( os.path.join( _path_batch_dir, '_' + str(_i) + '.sh'),'w') as _shell_script:
          _shell_script.write(_shell_template)

        # ---------------
        # condor_template
        if self.batch == 'condor':

          with open(os.path.join(self.path_templates, 'condor.txt'), 'r') as _condor_template_file:
            _condor_template = _condor_template_file.read()

          _replace_strings_condor = {
            '<name>'                 : os.path.join( _path_batch_dir, '_' + str(_i)),
            '<working_directory>'    : _path_batch_dir,
          }

          for _r, _rw in _replace_strings_condor.iteritems():
            _condor_template = _condor_template.replace(_r, _rw)

          with open( os.path.join( _path_batch_dir, '_' + str(_i) + '.txt'),'w') as _condor_script:
            _condor_script.write(_condor_template)
    
        if self.tree_production == 'Pixel':

          # self.print_nice('status', 'Pixel jobs made!')

          # Add pixel_template
          with open(os.path.join(self.path_templates, 'pixel_{0}.py'.format(self.script_template)), 'r') as _python_template_file:
            _python_template      = _python_template_file.read()

          _replace_strings_python = {
            '<number_of_events>'            : self.number_of_events,
            '<source_root_file_name>'       : _f,
            '<output_root_file_name>'       : 'PixelTree_' + _rr + '_' + str(_i) + '.root',
            '<global_tag>'                  : self.global_tag,
          }

          for _r, _rw in _replace_strings_python.iteritems():
            _python_template = _python_template.replace(_r, _rw)

          with open( os.path.join( _path_batch_dir, '_' + str(_i) + '.py'),'w') as _python_script:
            _python_script.write(_python_template)

          self.print_nice('status', 'Done: {0}'.format(os.path.join( _path_batch_dir, '_' + str(_i) + '.py')))

        elif self.tree_production == 'LA':
          self.print_nice('status', 'LA jobs!')
          # Add LA_template

        else:
          self.print_nice('error', 'Incorrect tree_production flag! Check self.tree_production!')
          continue

        # Sending jobs
        if self.send_jobs:

          if self.batch == 'condor':
            _condor_command = 'condor_submit ' + _path_batch_dir + '/_' + str(_i) + '.txt'
            self.print_nice('status', _condor_command)
            sp.call( _condor_command, shell=True)

          elif self.batch == 'lxbatch':
            _q              = 'cmscaf1nd' # queue for batch
            _batch_command  = 'bsub -R \"pool>30000\" -q ' + _q + ' -J ' + _rr + '_' + str(_i) + ' < ' + _path_batch_dir + '/_' + str(_i) + '.sh'
            self.print_nice('status', _batch_command)
            sp.call( _batch_command, shell=True)

  def print_nice(self, print_type, *text):

    try:

      if print_type == 'python_info': # Bright Yellow
        print '\033[1;33;40m' + ''.join(text) + '\033[0m'

      elif print_type == 'error':  # Bright Red
        print '\033[1;31;40m' + ''.join(text) + '\033[0m'

      elif print_type == 'status': # Bright Green
        print '\033[1;32;40m' + ''.join(text) + '\033[0m' 

    except Exception, e:
      print text

  def make_directory(self, directory):

    if not os.path.exists(directory):

      try:
        os.makedirs(directory)
      except OSError:
        if not os.path.isdir(directory):
          raise

    return directory

if __name__ == '__main__':

  t = TreeProduction()
  t.get_list_of_input_files()
  t.make_directory_eos()
  t.make_send_jobs()
