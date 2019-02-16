from distutils.core import setup, Extension

module = Extension("perm", sources = ["perm.c"])
setup (ext_modules = [module])
