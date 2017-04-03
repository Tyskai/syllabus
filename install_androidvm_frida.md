STEP 1: Installing Androlab VM
 
1.       Install VirtualBox
2.       Download androlab VM image from here: https://github.com/sh4hin/Androl4b
3.       Launch the image in VirtualBox by opening  the andro.vbox file just downloaded and pressing “Start”.
 
As indicated in the github page, the login/password combination is andro/androlab .
 
STEP 2: Downloading Android 4.4.2 and creating emulator
 
Open a console and run android . You’ll get into the SDK Manager.
 
Find and select the following packages under Android 4.4.2 (API 19):
·         SDK platform
·         ARM EABI v7a System Image
 
Then click Install, accept the licenses and wait for the download to finish. If you have trouble finding the ARM EABI system image, you may need to first install the SDK platform, then close the SDK manager and run it again.
 
After both these packages are installed, go the Tools menu and select “Manage AVDs”, press “Create…” and select the following settings:
 
cid:image003.jpg@01D2ABBD.56123C50
 
Press OK, and OK again in the final dialog.
 
After this, you should be able to load the emulator by running the following command in a console:
 
/home/andro/Android/Sdk/tools/emulator -avd lab2
 
Note that this is expected to take some time to boot. You should immediately see an emulator window with Android written in it. Once it’s finished booting you should see an emulated Android device as shown here:
 
cid:image004.jpg@01D2ABBD.56123C50
 
STEP 3: Installing Frida
 
From a console, run the following command:
 
sudo pip install frida
 
After this, try running frida --version to verify that it was correctly installed:
 
andro@lab:/tmp/test/APK % frida --version
9.1.25
andro@lab:/tmp/test/APK %
 
And we’re done
