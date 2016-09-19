# ICU
####I see you 

Home security application.  Includes source code for raspberry pi, API, server, and front end.

###To set up dev environment on your machine
1. [Install vagrant](https://www.vagrantup.com/docs/installation/)
2. Inside of git repo, start vagrant box:
  
  > vagrant up
3. Make sure you can ssh into the vagrant box:
  > vagrant ssh

`vagrant up` should be sufficient to get your dev env up and running. The Vagrantfile defines all of the settings for the box when it is spun up. Notice at the bottom of the vagrant file the line `config.vm.provision :shell, path: "bootstrap.sh"`.  This tells the box to run the `bootstrap.sh` script once the box is spun up.  If you need something to be automatically installed, add the commands in the bootstrap.sh file, and of course push up to master so we can all see the new dev env changes you've made :).
