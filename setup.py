from setuptools import setup, find_namespace_packages

setup(name='helper',
      version='1',
      description='Helper description',
      url='https://github.com/Kostenko-python-hw/project_group_9',
      author='Goit team',
      author_email='test@test.com ',
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['helper = helper_bot.main:main']},
      install_requires=['prompt_toolkit'])
