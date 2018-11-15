from distutils.core import setup, Extension

module1 = Extension('boardmodule',
                    sources = ['boardmodule.c'])

setup (name = 'BoardUpdater',
       version = '1.0',
       description = 'Package to update the board faster',
       ext_modules = [module1])
