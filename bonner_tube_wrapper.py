from bonner_tube_template import template
import numpy as np
from multigroup_utilities import energy_groups
import os






def write_input(erg_bounds, mat, template):
    """Writes an mcnp input file."""
    mats = {}
    mats['abs'] = (3, 1.070)
    mats['poly'] = (4, 1.300)
    template = template.format(*mats[mat], *mats[mat], *erg_bounds)
    with open('input.i', 'w+') as F:
        F.write(template)
    return


def run_input():
    """Runs the mncp input file."""
    print('run_input not implemented yet.')
    return

def extract_output():
    """Grabs the output value from the mcnp output file."""
    print('extract_output not implemented yet.')
    return

def clean_repo():
    """Removes the mcnp files from the repository."""
    for f in ['input.i', 'input.io', 'input.ir']:
        try:
            os.system('rm {}'.format(f))
        except:
            pass
    return



if __name__ == '__main__':
    eb = energy_groups()[::-1]*1e-6
    for i in range(len(eb)-1):
        write_input((eb[i],eb[i+1]), 'abs', template)
        run_input()
        extract_output()
        clean_repo()
