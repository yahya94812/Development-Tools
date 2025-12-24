# Creating and using ubuntu_virtual_machine in Ubuntu
* sudo apt update
* sudo apt install qemu-system-x86 qemu-utils //installing virtualization software
* qemu-img create -f qcow2 ubuntu_virtual_machine.img 10G //creating virtual hard disk of file format "qcow2" of name ubuntu_virtual_machine.img of 10GB
* qemu-system-x86_64 -m 2048 -cdrom /home/mohammed-yahya/My-Files/ubuntu-24.04.2-live-server-amd64.iso -boot d -hda ubuntu_virtual_machine.img //this command install ubuntu on virtual hard disk(it is a file) and ram is specified using -m 2048 approx 2GB
* qemu-system-x86_64 -m 2048 -hda ubuntu_virtual_machine.img //to boot directly from the virtual disk