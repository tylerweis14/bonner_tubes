from mcnp_template import template
from run_mcnp import run_mcnp
from driver import Filter_Job


# create a unit test for the response function style input file
job = Filter_Job('HDPE', 1.0, 0, 'In', '')
job.assign_erg('dummystruct', 0, 1, 10)

run_mcnp(job, template, inp_only=True)


# create a unit test for the integral response style input file
job = Filter_Job('HDPE', 1.0, 0, 'In', '', 'ir')

run_mcnp(job, template, inp_only=True)
