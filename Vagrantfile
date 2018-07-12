# -*- mode: ruby -*-
# vi: set ft=ruby :

# Ensure a minimum Vagrant version to prevent potential issues.
Vagrant.require_version '>= 1.5.0'

# Configure using Vagrant's version 2 API/syntax.
Vagrant.configure(2) do |config|
  config.vm.box = 'ubuntu/xenial64'
  config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"

  config.vm.provider "virtualbox" do |v|
    v.memory = 4096
    v.cpus = 4
  end

  config.vm.network "private_network", ip: "192.168.50.6"
  config.vm.synced_folder ".", "/home/vagrant/prattle"

  # Provision a development environment.
  config.vm.provision :shell do |sh|
    sh.inline = <<-EOF
      export DEBIAN_FRONTEND=noninteractive;

      # Additional PPAs etc
      sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
      echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
      sudo apt-get update --assume-yes;

      # OS packages
      sudo apt-get -y --allow-unauthenticated install git make \
      python-dev python-pip python3.4 libpq-dev mongodb-org;

      # Install python build dependencies
      sudo pip install virtualenv tox;
    EOF
  end
end
