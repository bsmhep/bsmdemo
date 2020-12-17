from bsm.util import safe_mkdir
from bsm.util import ensure_list
from bsm.util import call_and_log

def run(param):
    source_dir = param['config_package']['path'].get('source', param['package_path']['main_dir'])
    build_dir = param['config_package']['path'].get('build', os.path.join(param['package_path']['main_dir'], 'build'))
    install_dir = param['config_package']['path'].get('install', param['package_path']['main_dir'])

    safe_mkdir(build_dir)


    cmake_args = param['action_param'].get('args', [])
    cmake_args = ensure_list(cmake_args)
    cmake_args = [p.format(**param['pkg_dir_list']) for p in cmake_args]

    cmake_args.insert(0, '-DCMAKE_INSTALL_PREFIX='+install_dir)

    cmake_var = param['action_param'].get('var', {})
    for k, v in cmake_var.items():
        full_value = v.format(**param['config_package_install_path'])
        full_arg = '-D{0}={1}'.format(k, full_value)
        cmake_args.append(full_arg)

    env = param.get('env')


    with open(param['log_file'], 'w') as f:
        cmd = ['cmake', source_dir] + cmake_args
        ret = call_and_log(cmd, log=f, cwd=build_dir, env=env)

    return {'success': ret==0, 'message': 'CMake exit code: {0}'.format(ret)}
