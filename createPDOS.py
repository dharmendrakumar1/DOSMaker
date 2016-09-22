#!/usr/bin/env python

import argparse
import numpy as np

def parseArgs():
    parser = argparse.ArgumentParser(description='Create a single plottable file for DOS, as well as all of the PDOS within a DOSCAR.')
    parser.add_argument('--file', '-f', type=str, help='The DOSCAR file to be read in.', required=True, dest='fileName')
    parser.add_argument('--start', '-s', type=int, help='The index of the atom you want to start with.', default=0, dest='startIndex')
    parser.add_argument('--end', '-e', type=int, help='The index of the atom you want to end with.', default=-1, dest='endIndex')
    parser.add_argument('--pdos', '-p', type=str, help='The output file name you want the PDOS in.', default='pdos.dat', dest='pdosFileName')
    parser.add_argument('--dos', '-d', type=str, help='The output file name you want the DOS in.', default='dos.dat', dest='dosFileName')
    return parser.parse_args()

def preReqChecks(args):
    if args.endIndex != -1:
        if args.endIndex < args.startIndex:
            print 'The ending index must be larger than the starting index, exiting...'
            exit(-1)
    try:
        f = open(args.fileName, 'r')
        data = f.readlines()
    except:
        print 'Something went wrong reading the file:', args.fileName
        print 'Exiting...'
        exit(-1)
    return data

def getAtomCount(data):
    return int(data[0].split()[0])

def removeGarbage(data):
    del data[:5]
    return data

def getDOS(data):
    points = int(data[0].split()[2])
    del data[0]
    DOS = np.empty(points)
    energies = np.empty(points)
    for i in range(points):
        stuff = data[i].split()
        DOS[i] = float(stuff[1])
        energies[i] = float(stuff[0])
    del data[:points]
    return zip(energies, DOS)

def dataFilter(elem):
    return len(elem.split()) != 5

def getPDOS(data, startIndex, endIndex):
    points = int(data[0].split()[2])

    energies = np.empty(points)
    s_pdos = np.zeros(points)
    px_pdos = np.zeros(points)
    py_pdos = np.zeros(points)
    pz_pdos = np.zeros(points)
    d1_pdos = np.zeros(points)
    d2_pdos = np.zeros(points)
    d3_pdos = np.zeros(points)
    d4_pdos = np.zeros(points)
    d5_pdos = np.zeros(points)

    p_pdos = np.zeros(points)
    d_pdos = np.zeros(points)

    data = filter(dataFilter, data)

    atom_index = 0
    for i, line in enumerate(data):
        if i % points == 0 and i != 0:
            atom_index += 1
        if atom_index >= startIndex and atom_index <= endIndex:
            index = i % points
            stuff = [float(x) for x in line.split()]
            energies[index] = stuff[0]
            s_pdos[index] += stuff[1]
            px_pdos[index] += stuff[2]
            py_pdos[index] += stuff[3]
            pz_pdos[index] += stuff[4]
            d1_pdos[index] += stuff[5]
            d2_pdos[index] += stuff[6]
            d3_pdos[index] += stuff[7]
            d4_pdos[index] += stuff[8]
            d5_pdos[index] += stuff[9]

            p_pdos[index] += px_pdos[index] + py_pdos[index] + pz_pdos[index]
            d_pdos[index] += d1_pdos[index] + d2_pdos[index] + d3_pdos[index] + d4_pdos[index] + d5_pdos[index]
    return zip(energies, s_pdos, px_pdos, py_pdos, pz_pdos, p_pdos, d1_pdos, d2_pdos, d3_pdos, d4_pdos, d5_pdos, d_pdos)

def writeToFile(fname, data, header):
    f = open(fname, 'w')
    f.write(header)
    for line in data:
        for elem in line:
            f.write('%f   ' % elem)
        f.write('\n')
    f.close()

def main():
    args = parseArgs()
    data = preReqChecks(args)
    n_atoms = getAtomCount(data)
    if args.endIndex == -1: args.endIndex = n_atoms
    removeGarbage(data)
    dos = getDOS(data)
    pdos = getPDOS(data, args.startIndex, args.endIndex)
    writeToFile(args.dosFileName, dos, '# energy   DOS\n')
    writeToFile(args.pdosFileName, pdos, '# energy     s          px         py         pz         p          d1         d2         d3         d4         d5         d\n')



if __name__ == '__main__':
    main()