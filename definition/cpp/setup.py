"""
python setup.py build_ext --inplace

"""


from distutils.core import setup, Extension

define_module = Extension('_define', sources=['def.cpp', 'def.i'])
setup(name='define', ext_modules=[define_module], py_modules=["define"])