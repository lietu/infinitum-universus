# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    # Every Vagrant virtual environment requires a box to build off of.
    config.vm.box = "ubuntu/trusty64"
    config.vm.boot_timeout = 30

    # SSH agent forwarding makes life easier
    config.ssh.forward_agent = true

    # Configure Salt stack
    config.vm.provision :salt do |config|
        config.install_type = 'stable'
    end

    # Define the vm
    vm_name = "iu"
    config.vm.define :iu do |iu|
        iu.vm.network :private_network, ip: "172.16.16.16"
        iu.vm.hostname = vm_name

        iu.vm.synced_folder "salt/roots/", "/srv/"
        iu.vm.synced_folder ".", "/src/"

        iu.vm.network :forwarded_port, guest: 80, host: 80, auto_correct: true

        iu.vm.provider "virtualbox" do |v|
            v.name = vm_name
            # Uncomment if you want to see the virtualbox Gui for this VM
            # v.gui = true
            v.customize ["modifyvm", :id, "--memory", "2048"]
            v.customize ["modifyvm", :id, "--cpus", "4"]
            v.customize ["modifyvm", :id, "--ioapic", "on"]
        end

        iu.vm.provision :salt do |config|
            config.minion_config = "salt/minion.conf"
            config.run_highstate = true
            config.verbose = false
            config.bootstrap_options = "-D"
            config.install_type = "git"
            config.install_args = "stable"
            config.temp_config_dir = "/tmp"
            config.colorize = true
            config.log_level = "warning"

            config.pillar({
                vagrant: "vagrant"
            })
        end
    end
end
