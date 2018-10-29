import numpy as np
from mcnp_template import template
from multigroup_utilities import energy_groups
import subprocess
import re


def cut_generator(length, n, mat):
    leng = length + 15
    p = ''
    s = ''
    cut = np.linspace(15, leng, n+2)
    cut = cut[:-1]
    cut = cut[1:]
    for i in range(n):
        surf = -(28+i) if i != n-1 else -21
        p += '{} {} {} {} {} {} IMP:N={}\n'.format(i+12, *mat, 27+i, surf, -18, (2)**i)
        s += '{} {} {}\n'.format(27+i, 'PX', cut[i])
    return p, s


def filter_generator(filter_type, n, fil=False):
    if filter_type == 'Gad':
        filter_type = '8 -7.9'
    elif filter_type == 'Cd':
        filter_type = '7 -8.65'
    if fil:
        j = '{} {} {} {} {} IMP:N={}'.format(21, filter_type, 40, -26, -24, 2**n)
    else:
        j = '{} {}  {} {} {} IMP:N={}'.format(21, 0, 40, -26, -24, 0)
    return j


def write_input(name, erg_bounds, mat, length, template, fil=''):
    """Writes an mcnp input file."""
    mats = {}
    mats['HDPE'] = (2, 0.950)
    mats['abs'] = (3, 1.070)
    mats['poly'] = (4, 1.300)
    l = 15 + length
    lengths = [(l + 2), l, (l + 1.5)]

    # number of splits
    n = 8
    p, s = cut_generator(length, n, mats[mat])
    j = filter_generator(fil, n, bool(fil))
    template = template.format(*mats[mat], j, p, *lengths, s, *erg_bounds)
    with open(name + '.i', 'w+') as F:
        F.write(template)
    return


def run_input(name):
    """Runs the mncp input file."""
    subprocess.call(['mcnp6', 'name={}.i'.format(name)])
    return


def extract_output(name):
    """Grabs the output value from the mcnp output file."""
    with open(name + '.io', 'r') as F:
        output = F.read()
    output = output.split('1tally')
    output0 = output[1]
    output1 = output[2]
    s = r'                 \d.\d\d\d\d\dE[+-]\d\d \d.\d\d\d\d'
    pattern = re.compile(s)
    results = re.findall(pattern, output0)
    r0 = results[0].split()
    flux_weighted_xs = float(r0[0])
    err = float(r0[1])
    return flux_weighted_xs, err


def clean_repo(name):
    """Removes the mcnp files from the repository."""
    for f in ['.i', '.io', '.ir']:
        subprocess.call(['rm', format(name + f)])
    return


def run_mcnp(name, erg_bounds, mat, l, template, fil='', inp_only=False):
    """Runs all the functions given in this repo."""
    write_input(name, erg_bounds, 'abs', l, template)
    if not inp_only:
        run_input(name)
        val, err = extract_output(name)
        clean_repo(name)
        return val, err


if __name__ == '__main__':
    eb = energy_groups()[::-1]*1e-6
    for i in range(len(eb)-1):
        if i == 60:
            result = run_mcnp('input', (eb[i], eb[i+1]), 'poly', 1, template, fil='Gad', inp_only=True)
            print(result)
