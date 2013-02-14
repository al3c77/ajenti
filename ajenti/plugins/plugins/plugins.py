from ajenti.api import *
from ajenti.plugins import manager, ModuleDependency, BinaryDependency
from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui.binder import Binder


@plugin
class PluginsPlugin (SectionPlugin):
    def init(self):
        self.title = 'Plugins'
        self.icon = 'cogs'
        self.category = ''
        self.order = 50

        # In case you didn't notice it yet, this is the Plugins Plugin Plugin
        self.append(self.ui.inflate('plugins:main'))

        def post_dep_bind(object, collection, item, ui):
            if not item.satisfied():
                installer = ui.find('fix')
                if item.__class__ == ModuleDependency:
                    installer.package = 'python-module-' + item.module_name
                if item.__class__ == BinaryDependency:
                    installer.package = item.binary_name
                installer.recheck()

        self.find('dependencies').post_item_bind = post_dep_bind

        self.binder = Binder(self, self.find('bind-root'))
        self.refresh()

    def refresh(self):
        self.plugins = sorted(manager.get_all().values())
        self.binder.reset().autodiscover().populate()