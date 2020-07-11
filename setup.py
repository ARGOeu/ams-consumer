from distutils.core import setup
import platform

NAME = 'argo-ams-consumer'


def get_ver():
    try:
        for line in open(NAME + '.spec'):
            if "Version:" in line:
                return line.split()[1]
    except IOError:
        print("Make sure that {} is in directory".format(NAME + '.spec'))
        raise SystemExit(1)


setup(
    name=NAME,
    version=get_ver(),
    author='SRCE',
    author_email='dvrcic@srce.hr',
    package_dir={'argo_ams_consumer': 'pymod/'},
    packages=['argo_ams_consumer'],
    url='https://github.com/ARGOeu/ams-consumer',
    description='argo-ams-consumer fetchs metric result messages from Argo Messaging System',
    data_files=[('/etc/argo-ams-consumer', ['config/ams-consumer.conf', 'config/metric_data.avsc']),
                ('/usr/bin/', ['bin/ams-consumerd']),
                ('/usr/lib/systemd/system/', ['init/ams-consumer.service'])]
)
