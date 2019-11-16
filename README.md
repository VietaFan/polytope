# polytope
An automatic testing program for debugging competitive programming solutions (e.g. for things like Codeforces, etc. where using pre-existing code is ok).

(The name is inspired by Codeforces's Polygon platform, and since I happen to be studying polytopes in my combinatorics class.)

usage: 
** put the files ptcompare.cpp, polytope.py, and ptgen.py in whichever folder has your solution source files

** edit ptgen.py so that it prints out the tests of whichever problem you're working on 
(save it in ptgenN.py for problem N for instance)

** now to test the program, run the following command:

./polytope.py ptgenN.py src1.cpp src2.cpp

where ptgenN.py is the name of your test generator and src1.cpp and src2.cpp are your source files

it'll print out output that's pretty self-explanatory explaining where stuff is

** (you only need to modify ptgen.py usually, unless there's a bug somewhere)

difference.txt shows test cases where the programs differ, dtests.txt has just the tests where they differ, d1output.txt has the outputs of the first program for those tests, d2output.txt has the outputs of the second program for those tests
tests.txt has all of the test cases generated by ptgen, output1.txt has the outputs of program1 for those test cases, output2.txt has the outputs of program 2 for those test cases
if the programs are src1.cpp and src2.cpp, this will create modified source files that run with polytope tests in src1_pt.cpp and src2_pt.cpp and will compile those
(the original source files and binaries will not be modified)

