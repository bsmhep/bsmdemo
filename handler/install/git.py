import os

from bsm.util import safe_mkdir
from bsm.util import safe_rmdir
from bsm.util import call_and_log

def run(param):
    version = param['version']
    url = param['action_param']['url']
    tag = param['action_param']['tag'].format(version=version)
    dst_dir = param['config_package']['path'].get('source', param['package_path']['main_dir'])

    safe_rmdir(dst_dir)
    safe_mkdir(dst_dir)

    with open(param['log_file'], 'w') as f:
        cmd = ['git', 'clone', url, dst_dir]
        ret = call_and_log(cmd, log=f, cwd=dst_dir)
        if ret != 0:
            return {'success': False, 'message': 'Git clone exit code: {0}'.format(ret)}

        cmd = ['git', 'checkout', tag, '-b', 'version']
        ret = call_and_log(cmd, log=f, cwd=dst_dir)
        if ret != 0:
            return {'success': False, 'message': 'Git checkout tag exit code: {0}'.format(ret)}

    safe_rmdir(os.path.join(dst_dir, '.git'))

    return {'success': ret==0, 'message': 'Git OK'}
