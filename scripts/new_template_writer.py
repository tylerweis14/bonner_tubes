from mcnp_template2 import template2
import numpy as np
from mcnp_template import template
from multigroup_utilities import energy_groups
import subprocess
import re

def string_template(name,erg_bounds,x,template2):
    cells = ''
    surface = ''
    tally = ''
    HDPE = '2 -1.300'
    void = '0'
    indium = '5 -7.310'
    surface +='{} {} {} -{} {} -{} IMP:N={}\n'.format(50,HDPE,20,34,33,18,1)
    for i in range(1,x-1):
        surface += '{} {} {} -{} {} -{} IMP:N={}\n'.format(1000+i, indium, 32+2*i, 33+2*i, 33, 23, 1)
        surface += '{} {} {} -{} {} -{} IMP:N={}\n'.format(10000+i, void, 32+2*i, 33+2*i, 23, 18,1)
        surface += '{} {} {} -{} {} -{} IMP:N={}\n'.format(100+i, HDPE, 33+2*i, 34+2*i, 33, 18, 1)
        tally += 'F{}4:N {}\n'.format(i, 1000+i)
        tally += 'FM{}4 1 5 102\n'.format(i,) 
    for i in range(1,x):
        cells += '{} PX {}\n'.format(32+2*i,15.25+i*.635)
        cells += '{} PX {}\n'.format(33+2*i, 15.25+i*.635+0.1)
    surface +='{} {} {} {} {} {} IMP:N={}\n'.format(100000, void, 34+2*(x-2),-16,33,-18,1)
    template = template2.format(surface,cells,*erg_bounds,tally)
    with open(name + '.i', 'w+') as F:
        F.write(template)
    return template

def extract_output(name,x):
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


def run_mcnp(name, eb, x, template2):
    """Runs all the functions given in this repo."""
    mcnp_name = name
    string_template(mcnp_name,eb,x,template2)
    run_input(mcnp_name)
    val, err = extract_output(mcnp_name,x)
    clean_repo(mcnp_name)
    return val, err
    
if __name__ == '__main__':
    eb = energy_groups()[::-1]*1e-6
    for i in range(len(eb)-1):
        if i == 60:
            result = run_mcnp('test', (eb[i], eb[i+1]), 10, template2)
            print(result)
    
    
    
    
    
    
    
    
    
    
    
    
    