#!/usr/bin/env -S python

import os
from pathlib import Path
import yaml

BASE_PATH = os.path.dirname("__file__")
N=0

with open('config/values.yml', 'r') as f:
    box_config = yaml.full_load(f)

f = open(Path(BASE_PATH + "Vagrantfile"), "w")
f.write("""# -*- mode: ruby -*-
# vi: set ft=ruby :

## Generated nodes from config.yml
nodes = [
"""
)
f.close()

for key, value in box_config['boxes'].items():
  if value.get('enabled'):
    f = open(Path(BASE_PATH + "Vagrantfile"), "a")
    f.write(f"""
{'{'}
    :node => "node{N}",
    :hostname => "{key}",
    :box => "{value.get('box')}",
    :cpu => {value.get('cpu')},
    :mem => {value.get('mem')},
    :custom_ip => "{value.get('custom_ip')}",
    :ssh_port => {value.get('ssh_port')}
{'},'}""")
    f.close()
    N=+1
  else:
      break
  
f = open(Path(BASE_PATH + "Vagrantfile"), "a")
f.write("""]

## User Settings from config.yml
""")
f.close()
   
for key, value in box_config['config'].items():
  f = open(Path(BASE_PATH + "Vagrantfile"), "a")
  if type(value) != str:
    f.write(f"""
{key} = {value}""")
  if type(value) == str:
    f.write(f"""
{key} = "{value}" """)
f.close()

f = open(Path(BASE_PATH + "Vagrantfile"), "a")
f.write("""

## Number of configured nodes.
N = """+str(N)+"""

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  ### Iterate over nodes
  (1..N).each do |node_id|
    nid = (node_id - 1)

    config.vm.define "node#{nid}" do |node|
      if enable_custom_boxes == "yes"
        box_set = "no"
        nodes.each do |custom_box|
          if custom_box[:node] == "node#{nid}"
            node.vm.box = custom_box[:box]
            box_set = "yes"
          end
        end
        if box_set == "no"
          node.vm.box = box
        end
      end
      if enable_custom_boxes == "no"
        node.vm.box = box
      end
      node.vm.provider "virtualbox" do |vb|
        if linked_clones == "yes"
          vb.linked_clone = true
        end
        if custom_cpu_mem == "no"
          vb.customize ["modifyvm", :id, "--cpus", server_cpus]
          vb.customize ["modifyvm", :id, "--memory", server_memory]
        end
        if custom_cpu_mem == "yes"
          nodes.each do |cust_node|
            if cust_node[:node] == "node#{nid}"
              vb.customize ["modifyvm", :id, "--cpus", cust_node[:cpu]]
              vb.customize ["modifyvm", :id, "--memory", cust_node[:mem]]
            end
          end
        end
        if desktop == "yes"
          vb.gui = true
          vb.customize ["modifyvm", :id, "--graphicscontroller", "vboxvga"]
          vb.customize ["modifyvm", :id, "--accelerate3d", "on"]
          vb.customize ["modifyvm", :id, "--ioapic", "on"]
          vb.customize ["modifyvm", :id, "--vram", "128"]
          vb.customize ["modifyvm", :id, "--hwvirtex", "on"]
        end
        if additional_disks == "yes"
          (1..additional_disks_num).each do |disk_num|
            dnum = (disk_num + 1)
            ddev = ("node#{nid}_Disk#{dnum}.vdi")
            unless File.exist?("#{ddev}")
              vb.customize ['createhd', '--filename', ("#{ddev}"), '--variant', 'Fixed', '--size', additional_disks_size * 1024]
            end
            vb.customize ['storageattach', :id,  '--storagectl', "#{additional_disks_controller}", '--port', dnum, '--device', 0, '--type', 'hdd', '--medium', "node#{nid}_Disk#{dnum}.vdi"]
          end
        end
      end
      node.vm.hostname = "node#{nid}"

      ### Set additional network adapters below
      if additional_nics == "yes"
        if additional_nics_dhcp == "no"
          (1..additional_nics_num).each do |nic_num|
            if custom_ip == "yes"
              node.vm.network :private_network, ip: node[:custom_ip]
            end
            if custom_ip == "no"  
              nnum = Random.rand(0..50)
              node.vm.network :private_network, ip: subnet+"#{subnet_ip_start + nid + nnum}"
            end
          end  
        end
        if additional_nics_dhcp == "yes"
          (1..additional_nics_num).each do |nic_num|
            node.vm.network :private_network, type: "dhcp"
          end
        end
      end

      ### Set port forwards below
      if enable_port_forwards == "yes"
        nodes.each do |pf|
          node.vm.network "forwarded_port", guest: 22, host: pf[:ssh_port], id: "ssh"
        end
      end
      if provision_nodes == "yes"
        if node_id == N
          node.vm.provision "ansible" do |ansible|
            ansible.limit = "all"
            ansible.playbook = playbook_path
          end
        end
      end
    end
  end
end
""")
f.close()