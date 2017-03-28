We are going to do model based test generation and execution on programs from the RERS 2016 and 2017 challenges.

The first step is to download and install fMBT:

fMBT - https://01.org/fmbt

The easiest way to get fMBT installed is on a Ubuntu (Linux) machine, because it just needs the following commands in the right order:

```
sudo apt-add-repository ppa:antti-kervinen/fmbt-devel
sudo apt-get update
sudo apt-get install fmbt*
```

That's all.

Then download and unpack the RERS challenge programs:

The RERS 2016 reachability problems - http://www.rers-challenge.org/2016/problems/Reachability/ReachabilityRERS2016.zip
The RERS 2017 reachability training problems - http://rers-challenge.org/2017/problems/training/RERS17TrainingReachability.zip

The archives contain highly obfuscated c and java code. 
You can compile those sources as they are, with any c language compiler. 

We are going to assume, in our tests, to have both the binaries and the specifications of the programs, expressed by state machines that have been given to the tester (namely the model used for model based testing). 
For the sake of this experiment, it is possible to use all state machines obtained from the learnlib assigment.

Assume you have a .dot file describing the model, you need to translate it into the fMBT modeling language (.aal file).
You can do it by using one of the three python scripts located in this directory:

```
```
