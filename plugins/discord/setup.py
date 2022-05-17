from setuptools import setup, find_packages

version = '1.0.6'

setup(
    name="alerta-discord",
    version=version,
    description='Alerta plugin for Discord Webhooks',
    url='https://github.com/alerta/alerta-contrib',
    license='MIT',
    author='Albin Sejimer',
    author_email='albin@albins.website',
    packages=find_packages(),
    py_modules=['alerta_discord'],
    install_requires=[
        'requests'
    ],
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'alerta.plugins': [
            'discord = alerta_discord:DiscordWebhooks'
        ]
    }
)
