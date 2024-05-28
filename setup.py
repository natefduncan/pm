from setuptools import setup, find_packages

def get_reqs():
    with open("./requirements.txt", "r") as f:
        return f.readlines()

setup(
    name='pm',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_reqs(),
    entry_points={
        'console_scripts': [
            'pm = pm.main:cli',
        ],
    },
)
