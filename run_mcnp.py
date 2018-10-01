from mcnp_template import template
from multigroup_utilities import energy_groups
import subprocess
import re


def write_input(name, erg_bounds, mat, length, template):
    """Writes an mcnp input file."""
    mats = {}
    mats['abs'] = (3, 1.070)
    mats['poly'] = (4, 1.300)
    l = 50 - length
    template = template.format(*mats[mat], *mats[mat], l, *erg_bounds)
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
    output = output.split('1tally')[1]
    s = r'                 \d.\d\d\d\d\dE[+-]\d\d \d.\d\d\d\d'
    pattern = re.compile(s)
    results = re.findall(pattern, output)
    r = results[0].split()
    return float(r[0]), float(r[1])


def clean_repo(name):
    """Removes the mcnp files from the repository."""
    for f in ['.i', '.io', '.ir']:
        subprocess.call(['rm', format(name + f)])
    return


def run_mcnp(name, erg_bounds, mat, l, template):
    """Runs all the functions given in this repo."""
    write_input(name, erg_bounds, 'abs', l, template)
    run_input(name)
    val, err = extract_output(name)
    clean_repo(name)
    return val, err


if __name__ == '__main__':
    eb = energy_groups()[::-1]*1e-6
    for i in range(len(eb)-1):
        if i == 60:
            result = run_mcnp('input', (eb[i], eb[i+1]), 'abs', template)
            print(result)
