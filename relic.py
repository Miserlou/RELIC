#! /usr/bin/env python

# _____________________.____    .____________    | Regular
# \______   \_   _____/|    |   |   \_   ___ \   | Expressions
#  |       _/|    __)_ |    |   |   /    \  \/   | Legislative
#  |    |   \|        \|    |___|   \     \____  | Information
#  |____|_  /_______  /|_______ \___|\______  /  | Council
#         \/        \/         \/           \/   

from jinja2 import Environment, FileSystemLoader
import argparse
import os
import json
import sunlight
import requests
import names

import settings

# Arguments
parser = argparse.ArgumentParser(description='RELIC. Command line law.\n')
parser.add_argument('demands_file', metavar='U', type=str,
               help='Demands file.')
parser.add_argument('-l', '--law_template', metavar='L', type=str,
               help='Law template. Default: default_resolution.law')
parser.add_argument('-e', '--email_template', metavar='E', type=str,
               help='Email template. Default: default_email.tpl')
parser.add_argument('-d', '--dry', action='store_true',
                    help='Dry run.')

args = parser.parse_args()
vargs = vars(args)
if not any(vargs.values()):
    parser.error('Please supply your demands!')

# Get demands
demands_filename = vargs['demands_file']
with open(demands_filename, "r") as demands_file:
    demands_lines=demands_file.read().replace('\n', '')

try:
    demands = json.loads(demands_lines)
except Exception, e:
    print e
    print demands_lines
    print "Could not parse demands."

email_template = vargs['email_template']
if email_template:
    email = True
else:
    email = False

law_template = vargs['law_template']
if not law_template:
    law_template = 'default_resolution.law'

dry = vargs['dry']

# Set up law
env = Environment(loader=FileSystemLoader(''))
template = env.get_template(law_template)
rendered_law = template.render(demands)
print "\n"
print rendered_law
print "\n"

# Write the law to file
with open(demands_filename.replace('.demands', '.txt'), "wb") as fh:
        fh.write(rendered_law)

# Get the senators/reps
sunlight.config.API_KEY = settings.SUNLIGHT_API_KEY
reps = sunlight.openstates.legislators()

for rep in reps:
    if rep.get('email'):

        variables = {}

        variables['rendered_law'] = rendered_law
        variables['rep'] = rep
        variables['demands'] = demands

        print dir(rep)
        variables['name'] = names.get_full_name()

        email = rep.get('email')
        tel = rep.get('tel')
        name = rep.get('full_name')
        org = rep.get('state').upper() + ' ' + rep.get('district') + '(' + rep.get('chamber', '') + ')'
        print "\n"
        print name
        print email
        print org

        import pdb
        pdb.set_trace()

        # Create the email
        if email:
            env = Environment(loader=FileSystemLoader(''))
            template = env.get_template(email_template)
            rendered_email = template.render(variables)
            print "\n"
            print rendered_email
            print "\n"

            # Send the email
            if not dry:
                requests.post(
                    "https://api.mailgun.net/v2/samples.mailgun.org/messages",
                    auth=("api", "key-3ax6xnjp29jd6fds4gc373sgvjxteol0"),
                    data={"from": "Excited User <excited@samples.mailgun.org>",
                          "to": ["devs@mailgun.net"],
                          "subject": "Hello",
                          "text": "Testing some Mailgun awesomeness!"})
            else:
                print "Dry run, skipping email."
