from bsm.util import ensure_list
from bsm.util import call_and_log

def run(param):
    build_dir = param['config_package']['path'].get('build', os.path.join(param['package_path']['main_dir'], 'build'))

    env = param.get('env')
    env_make = env.copy()
    for k, v in param['action_param'].get('env', {}).items():
        env_make[k] = v.format(**param['config_package_install_path'])


    with open(param['log_file'], 'w') as f:
        cmd = ['make']
        ret = call_and_log(cmd, log=f, cwd=build_dir, env=env_make)

    return {'success': ret==0, 'message': 'Make exit code: {0}'.format(ret)}
