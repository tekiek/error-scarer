# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.require_version '>=1.7.4'

BUZZFEED_ROOT = '/opt/buzzfeed'

bfdeploy_script = <<EOF
echo "creating bfdeploy user"
if ! grep -q bfdeploy /etc/passwd; then
    groupadd -g 1010 bfdeploy
    useradd -d /home/bfdeploy -g bfdeploy -m -u 1010 -s /bin/bash bfdeploy
fi
mkdir -p ~bfdeploy/.ssh/
touch ~bfdeploy/.ssh/authorized_keys
chown -R bfdeploy:bfdeploy ~bfdeploy
EOF

bfdeploy_keys_script = <<EOF
echo "copy vagrant pubkey into bfdeploy user's authorized_keys..."
sudo cat /home/vagrant/.ssh/authorized_keys >> /home/bfdeploy/.ssh/authorized_keys
EOF

def chef_path(path)
  File.join(BUZZFEED_ROOT, 'chef', path)
end

def deploy_path(path)
  File.join(BUZZFEED_ROOT, 'mono/deploy', path)
end

# TODO: Figure out a better way to ensure that everything a VM needs to be
# provisioned is in place. Should we do away with this sort of global host->VM
# sharing of the /opt/buzzfeed dir, and require each VM to be totally self-
# contained (and thus require that git checkouts be part of the VM provisioning
# process)?
def require_repos(repo_names)
  missing_repos = repo_names.select do |repo_name|
    not Dir.exists?(File.join(BUZZFEED_ROOT, repo_name, '.git'))
  end
  if missing_repos.size > 0
    puts "These git repositories should be checked out to #{BUZZFEED_ROOT}:\n\n"
    missing_repos.each do |repo_name|
      expected_path = File.join(BUZZFEED_ROOT, repo_name)
      puts "\tgit clone git@github.com:buzzfeed/#{repo_name}.git #{expected_path}"
    end
    puts "\nMake sure those repositories exist and try again."
    exit 1
  end
end

require_repos(%w(chef error_scarer))

Vagrant.configure('2') do |config|
  config.vm.box = 'hashicorp/precise64'
  config.vm.hostname = 'dev.buzzfeed.org'
  config.vm.network :private_network, ip: '10.32.32.10'

  config.ssh.forward_agent = true

  # use default ~/.vagrant.d/insecure_private_key instead of letting vagrant
  # generate per-VM private keys, for easier ssh access without `vagrant ssh`
  config.ssh.insert_key = false

  config.vm.provider 'virtualbox' do |v|
    v.memory = 1536    # 1.5gb since bf-percona is memory intensive
    v.cpus = 2
    v.auto_nat_dns_proxy = false
    v.customize ['modifyvm', :id, '--natdnsproxy1', 'off']
    v.customize ['modifyvm', :id, '--natdnshostresolver1', 'off']
  end

  config.vm.synced_folder BUZZFEED_ROOT, BUZZFEED_ROOT, owner: 1010, group: 1010, create: true
  config.vm.provision 'shell', :inline => bfdeploy_script

  # first provision with chef to do systemwide setup
  config.vm.provision 'chef_solo' do |chef|
    chef.version = '12.5.1'
    chef.channel = 'stable' if Vagrant::VERSION =~ /^1\.8/
    chef.verbose_logging = true
    chef.log_level = 'debug'

    chef.cookbooks_path = chef_path('cookbooks')
    chef.roles_path = chef_path('roles')
    chef.environments_path = chef_path('environments')
    chef.data_bags_path = chef_path('data_bags')
    chef.environment = 'development'

    chef.add_recipe('pixiedust')
    chef.add_recipe('pixiedust_api')
    chef.add_recipe('pixiedust_admin')
    chef.add_recipe('error_scarer')

    chef.encrypted_data_bag_secret_key_path = '~/.ssh/MONO_encrypted_data_bag_secret'
  end

  config.vm.provision 'shell', :inline => bfdeploy_keys_script

  applications = ['error_scarer', 'mono']

  applications.each do |app|
    config.vm.provision 'ansible' do |ansible|
      ansible.inventory_path = 'ansible_vm_inventory'
      ansible.playbook = deploy_path(app + '_deploy.yml')
      # our deploy playbooks require some host pattern to be passed as an extra
      # var, so we pass hosts=all to apply run all plays on the VM
      ansible.extra_vars = {
        hosts: 'all',
        roles: 'all',
        perform_git_sync: false,
        perform_pip_install_dev_requirements: true,
        # ansible should log in as bfdeploy
        ansible_ssh_user: 'bfdeploy',
      }
    end
  end
end
