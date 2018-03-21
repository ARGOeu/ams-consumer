# argo-ams-consumer

## Description

`argo-ams-consumer` component fetchs metric results from ARGO Messaging Service and writes them into avro serialized files. Files are written on daily basis and represent full daily log of metric results formed and sent from Nagios monitoring instances.

Component is mainly serving for redundancy/backup of metric results within ARGO framework in case of erroneous behaviour of Flink/HBase stack.

## Installation

Component is supported on Centos 6 and Centos 7. RPM packages and all needed dependencies are available in ARGO repositories so installation of component simply narrows down to installing a package:

	yum install -y argo-ams-consumer 

For its functioning, component depends on:
- `argo-ams-library` - interaction with ARGO Messaging 
- `avro` - avro serialization of messages' payload
- `python-argparse` - ease build and parse of command line arguments
- `python-daemon` - ease daemonizing of component 

| File Types        | Destination                                        |
|-------------------|----------------------------------------------------|
| Configuration     | `/etc/argo-ams-consumer/ams-consumer.conf`         |
| Avro Schema       |  `/etc/argo-ams-consumer/metric_data.avsc`         |
| Daemon component  | `/usr/bin/ams-consumerd`                           |
| Init script (C6)  | `/etc/init.d/ams-consumer `                        |
| Service unit (C7) | `/usr/lib/systemd/system/ams-consumer.service`     |
| Pid files         | `/var/run/argo-ams-consumer/`                      |
| Log files         | `/var/log/argo-ams-consumer/`                      |
| Daily logs        | `/var/lib/argo-ams-consumer/`                      |
