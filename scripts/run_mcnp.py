import numpy as np
from source_template import rf_source, ir_source
from tally_template import rf_tally, ir_tally
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
    if filter_type == 'Gd':
        filter_type = '8 -7.9'
    elif filter_type == 'Cd':
        filter_type = '7 -8.65'
    if fil:
        j = '{} {} ({} {} {}):({} {} {}) IMP:N={}'.format(21, filter_type, 45, -44, -24, 26, -17, -24, 2**(n - 1))
    else:
        j = '{} {}  ({} {} {}):({} {} {}) IMP:N={}'.format(21, 0, 45, -44, -24, 26, -17, -24, 2**(n - 1))
    return j


def card_writer(card, data, elements):
    '''
    Function: card_writer

    This will write multiline cards for SI and SP distributions for mcnp inputs

    Input Data:
        card - name and number of the card
        data array - a numpy array containing the data you'd like placed in the card.
        Outputs:
            a string that can be copied and pasted into an mcnp input file
    '''
    s = '{}   '.format(card)
    empty_card = '   ' + ' ' * len(card)
    elements_per_row = elements
    row_counter = 0
    element = '{:6}  ' if data.dtype in ['int32', 'int64'] else '{:14.6e}  '
    for i, d in enumerate(data):
        s += element.format(d)
        row_counter += 1
        if row_counter == elements_per_row and i + 1 != len(data):
            row_counter = 0
            s += '\n{}'.format(empty_card)
    s += '\n'
    return s


def write_input(name, erg_bounds, mat, foils, length, template, job_type, group_struct, fil=''):
    """Writes an mcnp input file."""
    foil = {}
    foil['Au'] = (9, 19.30)
    foil['Mo'] = (10, 10.28)
    foil['In'] = (5, 7.310)
    mats = {}
    mats['HDPE'] = (2, 0.950)
    mats['abs'] = (3, 1.070)
    mats['poly'] = (4, 1.300)
    l = 15 + length
    lengths = [(l + 2), l, (l + 1.95), (l + 1.80), (l + 1.75), (l + 10)]

    # number of splits
    n = 8
    p, s = cut_generator(length, n, mats[mat])
    j = filter_generator(fil, n, bool(fil))

    # handle source term if used to calc rf or activity
    if job_type == 'rf':
        src_bounds = '{:8.6e} {:8.6e}'.format(*erg_bounds)
        src_prob = '0 1'
        source = rf_source.format(src_bounds, src_prob)
    elif job_type == 'ir':
        source = ir_source

    # consider tally
    if job_type == 'rf':
        tally = rf_tally.format(foil[foils][0])
    elif job_type == 'ir':
        groups = energy_groups(group_struct)[::-1] * 1E-6
        erg_card = card_writer('E4 ', groups, 4)
        tally = ir_tally.format(foil[foils][0], erg_card)

    template = template.format(*mats[mat], *foil[foils], j, p, *lengths, s, source, tally)
    with open(name + '.i', 'w+') as F:
        F.write(template)
    return


def run_input(name, job_type):
    """Runs the mncp input file."""
    if job_type == 'rf':
        subprocess.call(['mcnp6', 'name={}.i'.format(name)])
    elif job_type == 'ir':
        subprocess.call(['mcnp6', 'name={}.i'.format(name), 'tasks 26'])
    return


def extract_output(name, job_type):
    """Grabs the output value from the mcnp output file."""
    with open(name + '.io', 'r') as F:
        output = F.read()
    output = output.split('1tally')
    output = output[1]
    if job_type == 'rf':
        s = r'                 \d.\d\d\d\d\dE[+-]\d\d \d.\d\d\d\d'
        pattern = re.compile(s)
        results = re.findall(pattern, output)
        r0 = results[0].split()
        val = float(r0[0])
        err = float(r0[1])
        return val, err
    elif job_type == 'ir':
        # grab groupwise data
        s = r'    \d.\d\d\d\dE[+-]\d\d   \d.\d\d\d\d\dE[+-]\d\d \d.\d\d\d\d'
        pattern = re.compile(s)
        results = re.findall(pattern, output)
        val = np.empty(len(results))
        err = np.empty(len(val))
        for i, line in enumerate(results):
            bound, value, error = line.split()
            val[i] = float(value)
            err[i] = float(error)

        # grab total data
        s = r'      total      \d.\d\d\d\d\dE[+-]\d\d \d.\d\d\d\d'
        pattern = re.compile(s)
        results = re.findall(pattern, output)
        tots = results[0].split()
        tot_val = float(tots[1])
        tot_err = float(tots[2])
        return val, err, tot_val, tot_err


def clean_repo(name):
    """Removes the mcnp files from the repository."""
    for f in ['.i', '.io', '.ir']:
        subprocess.call(['rm', format(name + f)])
    return


def run_mcnp(job, template, inp_only=False):
    """Runs all the functions given in this repo."""
    if job.job_type == 'rf':
        mcnp_name = job.name + str(job.group_number)
    elif job.job_type == 'ir':
        mcnp_name = job.name
    write_input(mcnp_name, job.eb, job.plug_material, job.foil_material, job.length,
                template, job.job_type, job.group_structure, job.filter_material)
    if not inp_only:
        run_input(mcnp_name, job.job_type)
        extracted_output = extract_output(mcnp_name, job.job_type)
        clean_repo(mcnp_name)
        return extracted_output
    else:
        return 'Input Written'
