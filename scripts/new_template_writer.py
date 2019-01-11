from mcnp_template2 import template2
import numpy as np
from mcnp_template import template
from multigroup_utilities import energy_groups
import subprocess
import re


def string_template(name, erg_bounds, x,  length,  template2):
    cells = ''
    surface = ''
    tally = ''
    HDPE = '2 -1.300'
    void = '0'
    indium = '5 -7.310'
    surface += '{} {} ({} {} {}):({} {} {} {})  IMP:N={}\n'.format(10, HDPE,
        32, -34, -18, 34, -35, 23, -18, 1)
    surface += '{} {} {} {} {} IMP:N={}\n'.format(
        11, indium, 34, -104, -23, 1)
    surface += '{} {} {} {} {} IMP:N={}\n'.format(
        50, void, 104, -35, -23, 1)
    for i in range(1, x-1):
        surface += '{} {} ({} -{} -{}):({} -{} {} {})  IMP:N={}\n'.format(
            10+2*i, HDPE, 33+2*i, 34+2*i, 18, 34+2*i, 35+2*i, 23, -18, 1)
        surface += '{} {} {} -{} -{} IMP:N={}\n'.format(
            11+2*i, indium, 34+2*i, 104+2*i, 23, 1)
        surface += '{} {} {} -{} -{} IMP:N={}\n'.format(
            50+i, void, 104+2*i, 35+2*i, 23, 1)
        tally += 'F{}4:N {}\n'.format(i, 11+2*i)
        tally += 'FM{}4 1 5 102\n'.format(i)
    for i in range(x):
        cells += '{} PX {}\n'.format(32+2*i, 14.75+i*length)
        cells += '{} PX {}\n'.format(102+2*i, 14.75+i*length+0.05)
        cells += '{} PX {}\n'.format(33+2*i, 14.75+i*length+0.1)
    surface += '{} {} {} {} {} IMP:N={}\n'.format(
        100000, void, 31+x*2, -16, -18, 1)
    template = template2.format(surface, cells, *erg_bounds, tally)
    with open(name + '.i', 'w+') as F:
        F.write(template)
    return template


def extract_output(name,  x):
    """Grabs the output value from the mcnp output file."""
    with open(name + '.io', 'r') as F:
        output = F.read()
    output = output.split('1tally')
    flux = []
    error = []
    for i in range(x-1):
        output0 = output[i]
        s = r'                 \d.\d\d\d\d\dE[+-]\d\d \d.\d\d\d\d'
        pattern = re.compile(s)
        results = re.findall(pattern, output0)
        r0 = results[0].split()
        flux_weighted_xs = float(r0[0])
        err = float(r0[1])
        flux.append(flux_weighted_xs)
        error.append(err)
    return flux[1:], error[1:]


def run_input(name):
    """Runs the mncp input file."""
    subprocess.call(['mcnp6', 'name={}.i'.format(name)])
    return


def clean_repo(name):
    """Removes the mcnp files from the repository."""
    for f in ['.i', '.io', '.ir']:
        subprocess.call(['rm', format(name + f)])
    return


def run_mcnp(name, eb, x, length, template2):
    """Runs all the functions given in this repo."""
    mcnp_name = name
    string_template(mcnp_name, eb, x, length, template2)
    run_input(mcnp_name)
    val, err = extract_output(mcnp_name, x)
#    clean_repo(mcnp_name)
    return val, err


if __name__ == '__main__':
    eb = energy_groups()[::-1]*1e-6
    for i in range(len(eb)-1):
        if i == 60:
            result = run_mcnp('test', (eb[i], eb[i+1]), 10, 2.54, template2)
            print(result)
