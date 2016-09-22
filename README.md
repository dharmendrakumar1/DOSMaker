# DOSMaker

The python script createPDOS.py extracts the various PDOS and DOS from DOSCAR files outputted by VASP. This builds on @itamblyn's script to also plot out the px, py, and pz orbitals as well as all of the different d orbitals. 

example:

$ ./createPDOS.py -f DOSCAR -s 10 -e 20 -d dos.dat -p pdos_10_20_atom_range.dat

This will calculate output the full DOS as well as the PDOS for atoms with indices in the range 10 <= x <= 20.

You can also type

$ ./createPDOS.py --help 

for more option descriptions.
