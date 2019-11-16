#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <vector>
using namespace std;

void write_bad_tests(string of1, string of2, string tf, vector<int> &diffs) {
	ifstream res1(of1), res2(of2), tests(tf);
	ofstream out1("d1output.txt"), out2("d2output.txt"), outT("dtests.txt");
	ofstream out_diff("difference.txt");
	int ntests;
	tests >> ntests;
	bool write;
	int vpos = 0;
	string line1, line2, linet;
	getline(tests, linet); // get rid of rest of first line
	getline(res1, line1); // get initial lines
	getline(res2, line2);
	getline(tests, linet);
	for (int t=1; t<=ntests; t++) {
		while (vpos < diffs.size() && diffs[vpos] < t) {
			vpos++;
		}
		if (vpos == diffs.size()) break;
		write = (diffs[vpos] == t);
		do {
			if (write) {
				outT << linet << "\n";
				out_diff << linet << "\n";
			}
			getline(tests, linet);
			if (tests.eof()) break;
		} while (linet.substr(0, 13) != "polytope-test");
		do {
			if (write) {
				out1 << line1 << "\n";
				if (line1.substr(0, 13) == "polytope-test") {
					out_diff << "prog1 output:\n";
				} else {
					out_diff << line1 << "\n";
				}
			}
			if (res1.eof()) break;
			getline(res1, line1);
		} while (line1.substr(0, 13) != "polytope-test");
		do {
			if (write) {
				out2 << line2 << "\n";
				if (line2.substr(0, 13) == "polytope-test") {
					out_diff << "prog2 output:\n";
				} else {
					out_diff << line2 << "\n";
				}
			}
			getline(res2, line2);
			if (res2.eof()) break;
		} while (line2.substr(0, 13) != "polytope-test");
		
	}
	out1.close(); out2.close(); outT.close(); out_diff.close();
	res1.close(); res2.close(); tests.close();
}

void compare_results(string outfile1, string outfile2, string testfile) {
	ifstream res1(outfile1), res2(outfile2), tests(testfile);
	int ntests;
	tests >> ntests;
	string line1, line2;
	vector<int> diffs;
	bool disagree;
	for (int test=0; test <= ntests; test++) {
		disagree = false;
		do {
			getline(res1, line1);
			getline(res2, line2);
			if (line1 != line2) {
				disagree = true;
			}
		} while (line1.substr(0, 13) != "polytope-test" &&
				 line2.substr(0, 13) != "polytope-test");
		while (line1.substr(0, 13) != "polytope-test") {
			disagree = true;
			if (res1.eof()) break;
			getline(res1, line1);
		}
		while (line2.substr(0, 13) != "polytope-test") {
			disagree = true;
			if (res2.eof()) break;
			getline(res1, line2);
		}
		if (disagree) {
			diffs.push_back(test);
		}
	}
	res1.close();
	res2.close();
	tests.close();
	if (diffs.size() == 0) {
		cout << "all tests ok!\n";
	} else {
		write_bad_tests(outfile1, outfile2, testfile, diffs);
		cout << "answers disagree\n";
		cout << "first disagreement: test " << diffs[0] << "\n";
		cout << "disagreements occurred on " << diffs.size() << " of " << ntests << " test cases\n";
		cout << "see difference.txt and {dtests.txt, d1output.txt, d2output.txt} for results\n";
	}
}

int main(int argc, char **argv) {
	if (argc == 4) {
		compare_results(argv[1], argv[2], argv[3]);
	}	
	else {
		cout << "usage: ptcompare outfile1 outfile2 testfile\n";
		cout << "can be called from the bash script polytope.sh\n";
	}
	return 0;
}
