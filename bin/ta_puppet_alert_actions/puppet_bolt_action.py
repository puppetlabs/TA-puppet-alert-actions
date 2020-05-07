# encoding = utf-8

import pie
import json

# # create our alert object to build the actual report
# helper.log_info("Assembling alert data")
# alert = {}
# alert['global'] = {}
# alert['param'] = {}
# alert['global']['puppet_enterprise_console'] = puppet_enterprise_console
# alert['global']['splunk_hec_url'] = splunk_hec_url
# alert['global']['bolt_user'] = puppet_bolt_user
# alert['global']['bolt_user_pass'] = puppet_bolt_user_pass
# alert['global']['puppet_bolt_server'] = notnone(puppet_enterprise_console, puppet_bolt_server, helper)
# alert['global']['puppet_action_hec_token'] = notnone(splunk_hec_token, puppet_action_hec_token, helper)
# alert['global']['timeout'] = timeout

# # Load the alert specific settings that are really the task we're running
# alert['param']['bolt_target'] = bolt_target
# alert['param']['task_name'] = task_name
# alert['param']['task_parameters'] = task_parameters
# alert['param']['puppet_environment'] = puppet_environment


def run_bolt_task(alert, helper):
  # load our URLs, we generate possible ones assuming the console hostname is valid
  # however if a user provides their own pdb or bolt url it goes here
  # this also allows for us to add an int_proxy feature in the future
  endpoints = pie.util.getendpoints(alert['global']['puppet_enterprise_console'])
  rbac_url = endpoints['rbac']

  # since we're swapping out this data upstream anyway
  bolt_endpoint = pie.util.getendpoints(alert['global']['puppet_bolt_server'])
  bolt_url = bolt_endpoint['bolt']

  puppet_environment = alert['param']['puppet_environment']
  splunk_hec_url = alert['global']['splunk_hec_url']
  puppet_action_hec_token = alert['global']['puppet_action_hec_token']
  bolt_target = alert['param']['bolt_target']
  task_name = alert['param']['task_name']
  task_parameters = alert['param']['task_parameters']

  # parse if we were given a hostname already
  if alert['global']['pe_console'] is not None and alert['global']['pe_console'] is not '':
    pe_console = alert['global']['pe_console']
  else:
    pe_console = endpoints['console_hostname']

  message = {
    'message': 'Running task {} on {} '.format(task_name,bolt_target),
    'action_type': 'task',
    'action_name': task_name,
    'action_parameters': task_parameters,
    'action_state': 'starting',
    'pe_console': pe_console,
  }

  helper.log_debug(message)

  # if this happens to be a puppet run causing this task to be fired
  #if alert['result']['transaction_uuid']:
  #  message['transaction_uuid'] = alert['result']['transaction_uuid']
  
  pie.hec.post_action(message, bolt_target, splunk_hec_url, puppet_action_hec_token)

  bolt_user = alert['global']['bolt_user']
  bolt_user_pass = alert['global']['bolt_user_pass']

  if alert['global']['timeout'] is not None and alert['global']['timeout'] is not '':
    task_timeout = alert['global']['timeout']
  else:
    task_timeout = 360

  try:
    token_lifetime = int(task_timeout) * 2
  except Exception as e:
    helper.log_error("Timeout must be an integer, '{}' was provided instead".format(task_timeout))

  auth_token = pie.rbac.genauthtoken(bolt_user,bolt_user_pass,'TA-puppet-alert-actions',rbac_url, timeout=token_lifetime)

  # note: parameters is expected as a text string, not json, so in sample alert json must be represented as:
  # "task_parameters": "{ \"name\": \"ntpd\", \"action\": \"status\"}"

  try:
    job = pie.bolt.reqtask(bolt_target,task_name,auth_token,puppet_environment,bolt_url,parameters=task_parameters)
    jobid = job['name']
    helper.log_debug('Bolt Talks successfully requested with ID of {}'.format(jobid))
  except Exception as e:
    helper.log_error('Unable to request bolt task before of {}'.format(e))

  try:
    jobresults = pie.bolt.getjobresult(jobid, auth_token, bolt_url, timeout=task_timeout)
  except Exception as e:
    helper.log_error('Job failed before of {}'.format(e))

  # right now we're only running tasks against a single target, but may have things in the future returing multiple nodes
  for result in jobresults['items']:
    rmessage = message
    rmessage['action_state'] = result['state']
    rmessage['joburl'] = 'https://{}/#/run/jobs/{}'.format(pe_console,jobid)
    rmessage['pe_console'] = pe_console
    rmessage['result'] = result['result']
    #rmessage['transaction_uuid'] = result['transaction_uuid'] or message['transaction_uuid']
    rmessage['start_timestamp'] = result['start_timestamp']
    rmessage['duration'] = result['duration']
    rmessage['finish_timestamp'] = result['finish_timestamp']

    if rmessage['action_state'] == 'finished':
      rmessage['message'] = 'Successfully ran task {} on {} '.format(task_name,result['name'])
      helper.log_debug(rmessage['message'])
    elif result['state'] == 'failed':
      rmessage['message'] = 'Failed to run task {} on {} '.format(task_name,result['name'])
      helper.log_error(rmessage['message'])
    else:
      rmessage['message'] = 'Something happened to task {} on {} that we have no idea about'.format(task_name,result['name'])
      helper.log_error(rmessage['message'])

    pie.hec.post_action(rmessage, result['name'], splunk_hec_url, puppet_action_hec_token)

# this is our interactive load option
# assumes you're running this library directly from the command line
# cat example_alert.json | python $thisfile.py

if __name__ == "__main__":
  import sys
  import json

  alert = json.load(sys.stdin)
  try:
    run_bolt_task_custom(alert)
  except KeyError:
    run_bolt_task(alert)
