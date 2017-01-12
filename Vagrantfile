# -*- mode: ruby -*-
# vi: set ft=ruby :
# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "bento/centos-6.8"
  #config.vm.box = "bento/centos-7.2"
  config.vm.provision :shell, path: "bootstrap.sh"
  config.vm.network :private_network, ip: "192.168.56.111"
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--name", "exchange-rpmbuild", "--memory", "4000"]
  end
end
