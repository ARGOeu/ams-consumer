# Changelog

## [2.0.0] - 2020-09-08

### Added

* ARGO-2261 ams-consumer retry on ack_sub also
* ARGO-2527 Use systemd instances for spawning of multiple tenant ams-consumers

### Fixed

* ARGO-2080 Refactor AMS clients to use retry ams-library feature

### Changed

* ARGO-2513 Drop Centos6/Python2 support

## [1.1.0] - 2019-11-08

### Fixed

* Fix dash typo in consumer systemd service file

### Changed

* ARGO-1262 Extend consumer schema with actual_data field

## [1.0.0] - 2018-02-20

### Added

* ARGO-1106 Pull interval as float
* ARGO-1092 AMS Consumer README
* ARGO-1069 AMS Consumer Centos7 support
* ARGO-1050 Connection timeout as config option
* ARGO-869 RPM packaging metadata
* ARGO-1036 report period fix
* ARGO-1036 Message retention logic
* ARGO-790 avro serialization of fetched data
* ARGO-971 AMS messages fetching loop
* ARGO-846 Introduce config parser with template config file
* ARGO-845 Daemonize worker process and register signal handlers
