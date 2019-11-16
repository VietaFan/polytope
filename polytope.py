#!/usr/bin/env python3
import os, sys

def parse_chunk(chunk):
	pieces = chunk.split('[')
	return pieces[0].strip(' \t\n;'), tuple(map(lambda x: int(x.strip(']; \t\n')), pieces[1:]))

MAX_SIZE = [None, 1000, 50, 10, 5]

def polytopize(fname, out_fname):
	fin = open(fname, 'r')
	fout = open(out_fname, 'w')
	
	lines = fin.readlines()
	fout.write('#define POLYTOPE_TESTING\n')
	
	ptstr1 = '''#ifdef POLYTOPE_TESTING
	int polytope_ntests;
	cin >> polytope_ntests;
	string polytope_sampstr;
	int tnum;
	for (int polytope_tn=1; polytope_tn <= polytope_ntests; polytope_tn++) {
		cout << "polytope-test " << polytope_tn << "\n";
		cin >> polytope_sampstr >> tnum;
	#endif'''
	
	ptstr2 = '''#ifdef POLYTOPE_TESTING
	}
	cout << "polytope-test end\n";
	#endif'''
	glob_vars = []
	container_types = {'vector', 'set', 'map', 'unordered_map', 'unordered_set', 'deque', 'list', 'stack', 'queue'}
	number_types = {'bool', 'int', 'uint64_t', 'int64_t', 'u64', 's64', 'double', 'float', 'char', 'short', 'long'}
	for line in lines:
		if line[0] in ['\t',' ','#','/']: continue
		pieces = line.split()
		if line.strip() == '' or line.strip()[-1] != ';': continue
		prefix = line.strip().split()[0].split('<')[0]
		if '>' in line:
			index = len(line)-1
			while line[index] != '>':
				index -= 1
			suffix = line[index+1:]
		else:
			suffix = line[len(prefix):]
		chunks = map(lambda x: x.strip().strip(';'), suffix.split(','))
		varnames = map(parse_chunk, chunks)
		if prefix in container_types:
			for v in varnames:
				glob_vars.append(('container', v))
		elif prefix in number_types:
			for v in varnames:
				glob_vars.append(('number', v))
		elif prefix == 'string':
			for v in varnames:
				glob_vars.append(('string', v))
	
	for line in lines:
		if line[:9] == 'int main(':
			fout.write('int main_orig('+line[9:])
		elif line[:13] == '#define DEBUG':
			continue
		else:
			fout.write(line)
	fout.write(r'''
int main() {
	int polytope_ntests;
	cin >> polytope_ntests;
	string polytope_sampstr;
	int tnum;
	for (int polytope_tn=1; polytope_tn <= polytope_ntests; polytope_tn++) {
		cout << "polytope-test " << polytope_tn << "\n";
		cin >> polytope_sampstr >> tnum;
''')
	for var_type, var_pair in glob_vars:
		index_str = ''
		for k in range(len(var_pair[1])):
			fout.write('\t'*(k+2)+'for (int i%s=0; i%s<%s; i%s++) {\n' % (k,k,min(var_pair[1][k],MAX_SIZE[len(var_pair[1])]),k))
			index_str += '[i%s]' % (k)
		if var_type == 'number':
			fout.write('\t'*(len(var_pair[1])+2)+'%s%s = 0;\n' % (var_pair[0], index_str))
		elif var_type == 'container':
			fout.write('\t'*(len(var_pair[1])+2)+'%s%s.clear();\n'% (var_pair[0], index_str))
		elif var_type == 'string':
			fout.write('\t'*(len(var_pair[1])+2)+'%s%s = "";\n'% (var_pair[0], index_str))
		if len(var_pair[1]) > 0: fout.write('\t\t'+'}'*len(var_pair[1])+'\n')
	fout.write('\t\tmain_orig();\n')
	fout.write(r'''    }
	cout << "polytope-test end\n";
	return 0;
}''')
	fout.close()		

if not os.path.exists('ptcompare'):
	print('compiling ptcompare')
	os.system('g++ -o ptcompare ptcompare.cpp')			

os.system('python3 %s > tests.txt' % (sys.argv[1]))
print('generated tests')

s = []
for n in [2,3]:
	old_str = ''
	pt_path = sys.argv[n][:-4]+'_pt.cpp'
	if os.path.exists(pt_path):
		old_file = open(pt_path)
		old_str = old_file.read()
		old_file.close()
	polytopize(sys.argv[n], pt_path)
	new_file = open(pt_path)
	new_str = new_file.read()
	new_file.close()
	#os.system('cp %s %s' % (sys.argv[n], sys.argv[n][:-4]+'_pt.cpp'))
	s.append(sys.argv[n][:-4]+'_pt')
	#os.system('python3 pttoggle.py '+s[n-2]+'.cpp on')
	if new_str == old_str:
		print('program %s unchanged: skipped compile' % (n-1))
	else:
		os.system('g++ -o %s %s.cpp' % (s[n-2], s[n-2]))
		print('compiled program %s' % (n-1))

for n in range(2):
	os.system('./%s < tests.txt > output%s.txt' % (s[n],n+1))
	print('ran program %s' % (n+1))

os.system('./ptcompare output1.txt output2.txt tests.txt')
