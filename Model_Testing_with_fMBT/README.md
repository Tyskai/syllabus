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
It is possible to use all state machines obtained from the learnlib assigment.

Assume you have a .dot file describing the model, you need to translate it into the fMBT modeling language (.aal file).
You can do it by using one of the three python scripts located in this directory:

```
python translate Problem10.dot Problem10.aal
# or
python add_knowledge Problem10.dot Problem10.aal
# or
python with_sut Problem10.dot Problem10.aal
```

The difference among the three versions is:
1) translate.py just translates the provided state machine into the fMBT format, without any connection to the System Under Test (SUT) and without any hint on how to generate test cases.
2) add_knowledge.py will translate the provided state machine into the fMBT format, still without any connection to the SUT. It includes hints which will help fMBT to not generate un-interesting test cases. It will reset the state machine if an error output has been fired. It won't generate the same invalid input again and again. It will reset the state machine sometimes, instead of generating just one very long sequence of inputs.
3) with_sut.py does everything is done by the previous scripts. It provides connection with the sut as well.
You can run all of them and see the differences in the generated .aal file. 
Since only the third script allows the connection with the SUT, we are going to use it to get the test executed. 

Then you have to teach fMBT you want 100% coverage of all states of your model, and that is achieved by filling the test.conf file:

```
model		= aal_remote(remote_pyaal -l "Problem10.log" "Problem10.aal")
adapter		= aal
heuristic	= mrandom(20,lookahead(3),80,random(1234))
coverage	= sum(usecase(["s9"](perm(1))),usecase(["s8"](perm(1))),usecase(["s3"](perm(1))),usecase(["s2"](perm(1))),usecase(["s1"](perm(1))),usecase(["s0"](perm(1))),usecase(["s7"](perm(1))),usecase(["s6"](perm(1))),usecase(["s5"](perm(1))),usecase(["s4"](perm(1))),usecase(["s19"](perm(1))),usecase(["s18"](perm(1))),usecase(["s13"](perm(1))),usecase(["s12"](perm(1))),usecase(["s11"](perm(1))),usecase(["s10"](perm(1))),usecase(["s17"](perm(1))),usecase(["s16"](perm(1))),usecase(["s15"](perm(1))),usecase(["s14"](perm(1))),usecase(["s22"](perm(1))),usecase(["s20"](perm(1))),usecase(["s21"](perm(1))))
pass		= coverage(inf)
on_pass		= exit(0)
on_fail		= exit(1)
on_inconc	= exit(2)
```

Then you execute the tests by entering the following command:

```
fmbt -l Problem10.log Problem10.aal
```

This will generate an output such as:

```
INPUT:  5
Expected output -> 26 Observed output -> 26
INPUT:  1
Expected output -> 21 Observed output -> 21
INPUT:  5
Expected output -> 22 Observed output -> 22
INPUT:  5
Expected output -> Invalid input: 5 Observed output -> Invalid input: 5
INPUT:  4
Expected output -> Invalid input: 4 Observed output -> Invalid input: 4
INPUT: <RESET>
INPUT:  2
Expected output -> Invalid input: 2 Observed output -> Invalid input: 2
INPUT:  3
Expected output -> Invalid input: 3 Observed output -> Invalid input: 3
INPUT:  4
Expected output -> 25 Observed output -> 25
INPUT:  1
Expected output -> Invalid input: 1 Observed output -> Invalid input: 1
INPUT: <RESET>
INPUT:  5
Expected output -> 26 Observed output -> 26
INPUT: <RESET>
INPUT:  2
Expected output -> Invalid input: 2 Observed output -> Invalid input: 2
INPUT: <RESET>
INPUT:  3
Expected output -> Invalid input: 3 Observed output -> Invalid input: 3
INPUT:  1
Expected output -> Invalid input: 1 Observed output -> Invalid input: 1
INPUT:  4
Expected output -> 25 Observed output -> 25
INPUT:  5
Expected output -> 25 Observed output -> 25
INPUT:  3
Expected output -> 20 Observed output -> 20

...


INPUT:  3
Expected output -> 23 Observed output -> 23
INPUT:  3
Expected output -> 23 Observed output -> 23
INPUT:  1
Expected output -> 21ERROR 37 Observed output -> 21
Assertion failure at adapter() of "i:1": AssertionError: 
Traceback (most recent call last):
  File "Problem10.wa.aal", line 223, in adapter of action "i:1"
    assert output == outcome

fail: unexpected response to input "i:1": unidentified result.

```

What happened here ?
