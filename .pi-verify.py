import os, pathlib, subprocess, sys
if len(sys.argv) > 1:
    os.chdir(sys.argv[1])
root = pathlib.Path.cwd()
logs = root / '.box' / 'verification'
logs.mkdir(parents=True, exist_ok=True)
env = os.environ.copy()
env['PATH'] = '/home/ctown-admin/.rustup/toolchains/1.99.0-x86_64-unknown-linux-gnu/bin:' + env['PATH']
steps = [('build', ['cargo', 'build', '--locked']), ('test', ['cargo', 'test', '--locked', '--no-fail-fast', '--', '--test-threads=1'])]
failed = False
for name, cmd in steps:
    with (logs / (name + '.log')).open('w') as f:
        result = subprocess.run(cmd, env=env, stdout=f, stderr=subprocess.STDOUT)
    print('COMMAND:', ' '.join(cmd), 'EXIT:', result.returncode, flush=True)
    text = (logs / (name + '.log')).read_text(errors='replace')
    for line in text.splitlines():
        if line.startswith(('test result:', 'error:', 'error[', 'error: failed', 'Caused by:')) or 'Finished `' in line:
            print(line, flush=True)
    if result.returncode:
        print('\n'.join(text.splitlines()[-35:]), flush=True)
    failed |= result.returncode != 0
sys.exit(int(failed))
