from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(name='python-comprasnet',
      version='0.1.0',
      description='Lib that scrap informations in Brazilian Governement`s system called ComprasNet',
      url='http://github.com/moacirmoda/python-comprasnet',
      author='Moacir Moda',
      author_email='moa.moda@gmail.com',
      license='MIT',
      packages=['comprasnet'],
      install_requires=requirements,
      zip_safe=False)