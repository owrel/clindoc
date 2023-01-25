import setuptools

setuptools.setup(
    name='clindoc',
    version='0.2.0',
    description='Documentation tool for Clingo',
    author='Potassco Solutions & Potsdam University',
    license='GNU GPLv3',
    packages=setuptools.find_packages(),
    install_requires=['sphinx',
                      'sphinx_rtd_theme',
                      'rstcloth',
                      'graphviz',
                      'clingo'
                      ],

)
