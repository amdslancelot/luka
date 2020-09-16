from setuptools import setup, find_packages
#from distutils.core import setup #this would pass "python setup.py install"

setup(name='luka',
      packages=find_packages(),
      package_data={'': ['logging.json']},
      py_modules=['connect', 'utils', 'printer', 'custom_log', 'bash_config_reader', 'json_byteify'],
      version='0.1beta',
      author='Lans Hung',
      author_email='lans.hung@oracle.com'
)

# Release command:
# $ python setup.py bdist_rpm
