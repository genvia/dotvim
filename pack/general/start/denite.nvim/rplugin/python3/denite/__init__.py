# =============================================================================
# FILE: denite.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# =============================================================================

from importlib.util import find_spec

if find_spec('vim'):
    import vim
elif find_spec('pynvim'):
    import pynvim
    vim = pynvim
else:
    import neovim
    vim = neovim

if hasattr(vim, 'plugin'):
    # Neovim only

    from denite.ui.default import Default

    @vim.plugin
    class DeniteHandlers(object):
        def __init__(self, vim):
            self._vim = vim

        @vim.function('_denite_init', sync=True)
        def init_python(self, args):
            self._uis = {}
            self._vim.vars['denite#_channel_id'] = self._vim.channel_id
            return

        @vim.function('_denite_start', sync=True)
        def start(self, args):
            try:
                ui = self.get_ui(args[1]['buffer_name'])
                return ui.start(args[0], args[1])
            except Exception:
                import traceback
                import denite.util
                for line in traceback.format_exc().splitlines():
                    denite.util.error(self._vim, line)
                denite.util.error(self._vim,
                                  'Please execute :messages command.')

        @vim.function('_denite_do_action', sync=True)
        def take_action(self, args):
            try:
                ui = self.get_ui(args[0]['buffer_name'])
                return ui._denite.do_action(args[0], args[1], args[2])
            except Exception:
                import traceback
                import denite.util
                for line in traceback.format_exc().splitlines():
                    denite.util.error(self._vim, line)
                denite.util.error(self._vim,
                                  'Please execute :messages command.')

        def get_ui(self, buffer_name):
            if buffer_name not in self._uis:
                self._uis[buffer_name] = Default(self._vim)
            return self._uis[buffer_name]
