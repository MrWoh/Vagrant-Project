# Vagrant-Project
Tool written in Python to help deploy vagrant machines with flexible configuration.

#### Requirements

- [Python](https://www.python.org/downloads/source/)
- [Pyenv](https://github.com/pyenv/pyenv)
- [Vagrant](https://www.vagrantup.com)
- [Virtualbox](https://www.virtualbox.org)

#### Purpose

Create multiple virtual customizable boxes to test different enviroments.

#### How do I get set up?

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Edit default values *(Optional)*:
```bash
    vagrant-project
    ├── config/
    │    └──values.yml
    ├── run.py
    └── ...
```

3. Run the following python script from project directory to generate Vagrantfile
```bash
./run.py
```

#### Commands

Start up
```bash
vagrant up
```

Shutdown boxes
```bash
vagrant halt
```

Destroy
```bash
vagrant destroy -f
```

#### Variables

| Name | Type | Description | Default |
|---|---|---|---|
| **box** | ***string*** | Default Vagrant box | "generic/centos9s" |
| **desktop** | ***bool*** | Set if running desktop OS | no |
| **enable_custom_boxes** | ***bool*** | Set if custom boxes should be used | Yes |
| **enable_port_forwards** | ***bool*** | Set if port forwards should be enabled | Yes |
| **linked_clones** | ***bool*** | Sets if nodes should be linked from master VM | no |
| **provision_nodes** | ***bool*** | Set if provisioners should run | no |
| **server_cpus** | ***integer*** | Set number of CPU cores | 1 |
| **server_memory** | ***integer*** | Set amount of memory to assign | 512 |
| **subnet** | ***string*** | Set subnet for private_network | "192.168.56." |
| **subnet_ip_start** | ***bool*** | Set starting last octet | 200 |
| **custom_ip** | ***bool*** | Define using custom ip | yes |
| **additional_disks** | ***bool*** | Set if additional drives Setd should be added | no |
| **additional_disks_controller** | ***string*** | Set disks controller | "SATA Controller" |
| **additional_disks_num** | ***integer*** | Set the number of additional disks to add | 1 |
| **additional_disks_size** | ***bool*** | Set disk size in GB | 2 |
| **additional_nics** | ***bool*** | Set if additional network adapters should be created | Yes |
| **additional_nics_dhcp** | ***bool*** | Set if additional network adapters should be DHCP assigned | Yes |
| **additional_nics_num** | ***integer*** | desc | 1 |
| **playbook_path** | ***bool*** | Set path to playbooks | "playbook.yml" |


#### Who do I talk to? ###

[Paulius Verseckas](mailto:paulius.verseckas@zenitech.co.uk)