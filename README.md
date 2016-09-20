# ICU
####I see you

Home security application.  Includes source code for raspberry pi, API, server, and front end.

###To set up dev environment on your machine
1. [Install vagrant](https://www.vagrantup.com/docs/installation/) on your machine.
2. Inside of git repo, start vagrant box:
> vagrant up

3. Make sure you can ssh into the box:
> vagrant ssh

4. Make sure apache is running and you can see the box in your network:
  
> Go to [http://127.0.0.1:4567/](http://127.0.0.1:4567/) in your browser
5. All files in the ICU repo will be synced with the vagrant machine, and stored under the `/vagrant` folder.  So if you make a change to this readme outside of the box (in the repo directory on your machine), and ssh in, you will see the change there in `/vagrant/README.md`.  The same is true the other way around.

`vagrant up` should be sufficient to get your development environment up and running. The Vagrantfile defines all of the settings for the box when it is spun up. Notice at the bottom of the vagrant file the line `config.vm.provision :shell, path: "bootstrap.sh"`.  This tells the box to run the `bootstrap.sh` script once the box is spun up, and installs what we want it to.  If you need something to be automatically installed on spin up, add the commands in the bootstrap.sh file, and of course push up to master so we can all see the new dev env changes you've made :).

For example, say you want ruby installed on the box. Go into bootstrap.sh and add this line at the end:
> sudo apt-get install ruby-full

To update your VM, use this command:
> vagrant reload --provision

This command is the same as you would enter manually if you were ssh'd into the box itself.  Be sure to include all the setup steps necessary so others can easily update their environemnts as well.  After that, push up the updated `bootstrap.sh` file so we can all have ruby too!


####Some useful commands to know:
* `vagrant up` starts the vagrant box
* `vagrant destroy`... destroys it
* `vagrant reload` restarts the box, but does not re-run the bootstrap.sh file
* `vagrant reload --provision` restarts the box and re-runs the bootstrap.sh file, because it is set as the provisioning file
* `vagrant ssh` allows you to ssh into the box and work inside of it

