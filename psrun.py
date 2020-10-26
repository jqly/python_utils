import os
import sys
import subprocess
import tempfile
import logging


logger = logging.getLogger(__name__)

def run_ps(cmds, *args, **kwargs):
    with tempfile.TemporaryDirectory() as temp_dir:
        script = 'script.ps1'
        script_path = os.path.join(temp_dir, script)
        with open(script_path, 'w') as fp:
            if isinstance(cmds, list):
                print('\n'.join(cmds), file=fp)
            elif isinstance(cmds, str):
                print(cmds, file=fp)
            else:
                raise TypeError(('run_ps: cmds must be '
                    'str or list of strs'))
        return subprocess.run(
            'powershell.exe "%s"' % script_path, 
            *args, **kwargs)


if __name__ == '__main__':
    logging.basicConfig(
        stream=sys.stdout, 
        level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    script = '''cd c:\\Users
ls'''

    ps_result = run_ps(script, stdout=subprocess.PIPE, text=True)
    print(ps_result.stdout)
