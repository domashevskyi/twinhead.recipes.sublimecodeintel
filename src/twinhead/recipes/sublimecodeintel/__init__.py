import os
import simplejson as json
import zc.recipe.egg


class SublimeCodeIntel(object):

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        wd = self.buildout['buildout']['directory']

        self._remote_path = self.options.get('remote_path', None)

        res = []
        develop_locations = self.buildout['buildout']['directory']
        for _path in develop_locations:
            res.append(os.path.normpath(os.path.join(wd, './src')))
        self._ignored_paths = res

        self._dpath = os.path.join(wd, '.codeintel')
        self._fpath = os.path.join(self._dpath, 'config')
        self._python = options.get('target_python', '/usr/bin/python')
        self._extra_paths = options.get('extra-paths',
                                        options.get('extra_paths', '')
                                        ).split('\n')
        self._app_eggs = filter(None, options['eggs'].split('\n'))
        self.egg = zc.recipe.egg.Egg(self.buildout, self.name, self.options)

    def install(self):
        #egg_names, ws = egg.working_set(self._app_eggs)
        _reqs, ws = self.egg.working_set()
        egg_paths = ws.entries + self._extra_paths
        # strip empty paths
        egg_paths = [p for p in egg_paths if p.strip() != '']

        # relocate eggs so paths are valid on remote computers
        # (via nfs, smb, ...)
        if self._remote_path is not None:
            prefix = self.buildout['buildout']['directory']
            prefix_length = len(prefix)
            egg_paths = [p.startswith(prefix) and \
                         '%s%s' % (self._remote_path, p[prefix_length:]) or p \
                         for p in egg_paths]

        #strip develop paths,they're probably in Eclipse source path
        egg_paths = filter(lambda p: p not in self._ignored_paths, egg_paths)

        if not os.path.exists(self._dpath):
            os.mkdir(self._fpath)
        f_open_type = 'r'
        if not os.path.exists(self._fpath):
            f_open_type = 'w'

        with open(self._fpath, f_open_type) as f:
            data = json.loads(f.read() or '{}')
            if not 'Python' in data:
                data['Python'] = {}
            if not 'python' in data['Python']:
                data['Python']['python'] = self._python
            data['Python']['pythonExtraPaths'] = egg_paths

        open(self._fpath, 'w').write(data)

        return ""

    update = install
