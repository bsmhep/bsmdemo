from bsm.util import ensure_list
from bsm.util import safe_mkdir
from bsm.util import call_and_log

def run(param):
    build_dir = param['config_package']['path'].get('build', os.path.join(param['package_path']['main_dir'], 'build'))
    install_dir = param['config_package']['path'].get('install', param['package_path']['main_dir'])

    safe_mkdir(install_dir)

    install_args = param['action_param'].get('args', ['install'])
    install_args = ensure_list(install_args)

    env = param.get('env')
    env_install = env.copy()
    for k, v in param['action_param'].get('env', {}).items():
        env_install[k] = v.format(**param['config_package_install_path'])


    with open(param['log_file'], 'w') as f:
        cmd = ['make'] + install_args
        ret = call_and_log(cmd, log=f, cwd=build_dir, env=env_install)

    return {'success': ret==0, 'message': 'Make install exit code: {0}'.format(ret)}
