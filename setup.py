from setuptools import setup, find_packages

setup(
    name='plano_amostral',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'scipy',
        'ipywidgets',
    ],
    entry_points={
        'console_scripts': [
            'calcular_plano=plano_amostral:main',
        ],
    },
    author='Seu Nome',
    author_email='seu.email@example.com',
    description='Uma ferramenta para calcular planos amostrais interativamente usando ipywidgets.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/seu-usuario/plano_amostral',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
