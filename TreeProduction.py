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

    self.dataset          = '/RelValMinBias_13/CMSSW_8_1_0-81X_upgrade2017_realistic_v26_HLT2017-v1/GEN-SIM-RECO' 
    self.run_number       = 'MC'
    self.CMSSW_version    = 'CMSSW_8_1_0'
    self.global_tag       = ''
    self.SCRAM_ARCH       = 'slc6_amd64_gcc530'

    self.tree_production  = 'Pixel' # 'LA', 'Pixel'
    self.force_all        = False
    self.number_of_events = '10'
    self.number_of_jobs   = 1

    self.path_working_dir = os.path.dirname(os.path.abspath(__file__))
    self.path_batch       = os.path.join(self.path_working_dir, 'batch', self.run_number)
    self.path_templates   = os.path.join(self.path_working_dir, 'templates')
    self.path_log_file    = os.path.join(self.path_working_dir, 'log.txt')
    self.path_destination = {
      'Pixel' : '/store/group/dpg_tracker_pixel/comm_pixel/PixelTree/2017/test',
      'LA'    : ''
    }

    self.list_of_input_files= []

    # When you call voms-proxy-init --voms cms --valid 168:00
    # As a result you get the output like /tmp/x509up_u78012
    # Then copy this x509up_u78012 wherever you want and this is voms_user_proxy
    self.voms_user_proxy  = '/afs/cern.ch/user/b/bmesic/x509up_u78012'


    self.print_nice('status', 'Dataset: {0}'.format(self.dataset))
    self.print_nice('status', 'Run number: {0}'.format(self.run_number))
    self.print_nice('status', 'CMSSW version: {0}'.format(self.CMSSW_version))
    self.print_nice('status', 'global tag: {0}'.format(self.global_tag))
    self.print_nice('status', 'SCRAM_ARCH: {0}'.format(self.SCRAM_ARCH))    

    self.print_nice('status', '\nWorking directory: {0}'.format(self.path_working_dir))

  # Not used right now
  def get_run_informations_using_DAS(self):
    self.print_nice('python_info', '\nCalled get_run_informations_using_DAS function.') 
    _command = ['/cvmfs/cms.cern.ch/common/das_client', '--query="config dataset={0}"'.format(self.dataset), '--format=JSON', '--das-headers']
    _output = json.loads(sp.check_output(' '.join(_command), shell=True).strip())
    print _output

  # working
  def initialise_VOMS(self):
    self.print_nice('python_info', '\nCalled initialise_VOMS function.')
    _command = ['voms-proxy-init', '--voms', 'cms', '--valid', '168:00']
    sp.call(_command)

  def get_list_of_input_files(self):
  
    self.print_nice('python_info', '\nCalled get_list_of_input_files function.')  

    self.make_directory(self.path_batch)
    _path_output_file = os.path.join(self.path_batch, self.run_number + '.txt')

    # If file does not exist or force redo call das_client
    if not os.path.exists(_path_output_file) or self.force_all:

      _output_file  = open(_path_output_file, 'w')
      # _command = ['/cvmfs/cms.cern.ch/common/das_client', '--query="file run={0} dataset={1}"'.format(self.run_number, self.dataset), '--limit=0']
      _command      = ['/cvmfs/cms.cern.ch/common/das_client', '--query="file dataset={0}"'.format(self.dataset), '--limit=0']
      _output       = sp.check_output(' '.join(_command), shell=True)
      print _output
      _output_file.write(_output)
      _output_file.close

    _output_file = open(_path_output_file, 'r')
    # self.list_of_input_files = _output_file.read().splitlines()
    self.list_of_input_files = ['a']*self.number_of_jobs
    _output_file.close

  def make_jobs(self):
    
    self.print_nice('python_info', '\nCalled make_jobs function.')  

    _path_batch_dir = os.path.join(self.path_batch, self.tree_production)
    self.make_directory(_path_batch_dir)

    for _i, _f in enumerate(self.list_of_input_files):

      # if _i > 0:
      #   continue

      # ---------------
      # shell_template

      _shell_template_file = open(os.path.join(self.path_templates, 'shell.sh'), 'r')
      _shell_template = _shell_template_file.read()
      _shell_template_file.close()

      _replace_strings_shell = {
        '<SCRAM_ARCH>'                : self.SCRAM_ARCH,
        '<X509_USER_PROXY>'           : self.voms_user_proxy,
        '<working_directory>'         : self.path_working_dir,
        '<path_python_file>'          : os.path.join( _path_batch_dir, '_' + str(_i) + '.py'),
        '<root_file_name>'            : 'PixelTree_' + self.run_number + '_' + str(_i) + '.root',
        '<root_file_name_destination>': self.path_destination[self.tree_production]
      }

      for _r, _rw in _replace_strings_shell.iteritems():
        _shell_template = _shell_template.replace(_r, _rw)

      _shell_script = open( os.path.join( _path_batch_dir, '_' + str(_i) + '.sh'),'w')
      _shell_script.write(_shell_template)
      _shell_script.close()


      if self.tree_production == 'Pixel':

        # self.print_nice('status', 'Pixel jobs made!')

        # Add pixel_template
        _python_template_file = open(os.path.join(self.path_templates, 'pixel.py'), 'r')
        _python_template      = _python_template_file.read()
        _python_template_file.close()

        _replace_strings_python = {
          '<number_of_events>'            : self.number_of_events,
          '<source_root_file_name>'       : _f,
          '<output_root_file_name>'       : 'PixelTree_' + self.run_number + '_' + str(_i) + '.root',
          '<global_tag>'                  : self.global_tag,
        }

        for _r, _rw in _replace_strings_python.iteritems():
          _python_template = _python_template.replace(_r, _rw)

        _python_script = open( os.path.join( _path_batch_dir, '_' + str(_i) + '.py'),'w')
        _python_script.write(_python_template)
        _python_script.close()

        self.print_nice('status', 'Done: {0}'.format(os.path.join( _path_batch_dir, '_' + str(_i) + '.py')))



      elif self.tree_production == 'LA':
        self.print_nice('status', 'LA jobs!')
        # Add LA_template

      else:
        self.print_nice('error', 'Incorrect tree_production flag! Check self.tree_production!')

  def send_jobs(self):

    self.print_nice('python_info', '\nCalled send_jobs function.')

    _path_batch_dir = os.path.join(self.path_batch, self.tree_production)

    # queue for batch
    _q = 'cmscaf1nd'

    for _i, _f in enumerate(self.list_of_input_files):

      if _i > self.number_of_jobs - 1 and self.number_of_jobs != -1:
        continue

      _batch_command = 'bsub -R \"pool>30000\" -q ' + _q + ' -J ' + self.run_number + '_' + str(_i) + ' < ' + _path_batch_dir + '/_' + str(_i) + '.sh'
      self.print_nice('status', _batch_command)
      sp.call( _batch_command, shell=True)

  def write_log_file(self):
    with open(self.path_log_file, "a") as _file:
        _file.write("appended text")
      # add all informations

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

if __name__ == '__main__':

  t = TreeProduction()
  # # t.initialise_VOMS() # Not used
  t.get_list_of_input_files()
  t.make_jobs()
  # t.send_jobs()
  # t.write_log_file()