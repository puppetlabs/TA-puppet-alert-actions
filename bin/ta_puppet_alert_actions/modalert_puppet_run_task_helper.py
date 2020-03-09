
# encoding = utf-8

import json
from puppet_bolt_action import run_bolt_task

# given a setting, check to see if the alert is configured with default override
def override(setting_name, helper):
    alert_setting = helper.get_param(setting_name)
    global_setting = helper.get_global_setting(setting_name)

    if alert_setting is not None and alert_setting is not '':
        final_value = alert_setting
        helper.log_debug("Alert value present for '{}' it is '{}'".format(setting_name, final_value))
    elif global_setting is not None and global_setting is not '':
        final_value = global_setting
        helper.log_debug("Alert value NOT present for '{}', using Global value '{}'".format(setting_name,final_value))
    else:
        helper.log_debug("There is no value, None returned")
        final_value = None
    
    return final_value

# function to make sure we only set values we know aren't None
def notnone(default_value, possible_none, helper):
    if possible_none is not None and possible_none is not '':
        helper.log_debug("notnone: True")
        return possible_none
    else:
        helper.log_debug("notnone: False")
        return default_value


def process_event(helper, *args, **kwargs):
    """
    # IMPORTANT
    # Do not remove the anchor macro:start and macro:end lines.
    # These lines are used to generate sample code. If they are
    # removed, the sample code will not be updated when configurations
    # are updated.

    [sample_code_macro:start]

    # The following example gets and sets the log level
    helper.set_log_level(helper.log_level)

    # The following example gets account information
    user_account = helper.get_user_credential("<account_name>")

    # The following example gets the setup parameters and prints them to the log
    puppet_enterprise_console = helper.get_global_setting("puppet_enterprise_console")
    helper.log_info("puppet_enterprise_console={}".format(puppet_enterprise_console))
    puppet_default_user = helper.get_global_setting("puppet_default_user")
    helper.log_info("puppet_default_user={}".format(puppet_default_user))
    splunk_hec_url = helper.get_global_setting("splunk_hec_url")
    helper.log_info("splunk_hec_url={}".format(splunk_hec_url))
    splunk_hec_token = helper.get_global_setting("splunk_hec_token")
    helper.log_info("splunk_hec_token={}".format(splunk_hec_token))
    bolt_user = helper.get_global_setting("bolt_user")
    helper.log_info("bolt_user={}".format(bolt_user))
    puppet_action_hec_token = helper.get_global_setting("puppet_action_hec_token")
    helper.log_info("puppet_action_hec_token={}".format(puppet_action_hec_token))
    puppet_bolt_server = helper.get_global_setting("puppet_bolt_server")
    helper.log_info("puppet_bolt_server={}".format(puppet_bolt_server))
    puppet_db_url = helper.get_global_setting("puppet_db_url")
    helper.log_info("puppet_db_url={}".format(puppet_db_url))
    timeout = helper.get_global_setting("timeout")
    helper.log_info("timeout={}".format(timeout))
    pe_console = helper.get_global_setting("pe_console")
    helper.log_info("pe_console={}".format(pe_console))

    # The following example gets the alert action parameters and prints them to the log
    bolt_target = helper.get_param("bolt_target")
    helper.log_info("bolt_target={}".format(bolt_target))

    task_name = helper.get_param("task_name")
    helper.log_info("task_name={}".format(task_name))

    task_parameters = helper.get_param("task_parameters")
    helper.log_info("task_parameters={}".format(task_parameters))

    puppet_environment = helper.get_param("puppet_environment")
    helper.log_info("puppet_environment={}".format(puppet_environment))

    puppet_enterprise_console = helper.get_param("puppet_enterprise_console")
    helper.log_info("puppet_enterprise_console={}".format(puppet_enterprise_console))

    bolt_user = helper.get_param("bolt_user")
    helper.log_info("bolt_user={}".format(bolt_user))

    pe_console = helper.get_param("pe_console")
    helper.log_info("pe_console={}".format(pe_console))

    puppet_bolt_server = helper.get_param("puppet_bolt_server")
    helper.log_info("puppet_bolt_server={}".format(puppet_bolt_server))

    puppet_db_url = helper.get_param("puppet_db_url")
    helper.log_info("puppet_db_url={}".format(puppet_db_url))

    timeout = helper.get_param("timeout")
    helper.log_info("timeout={}".format(timeout))

    splunk_hec_url = helper.get_param("splunk_hec_url")
    helper.log_info("splunk_hec_url={}".format(splunk_hec_url))

    puppet_action_hec_token = helper.get_param("puppet_action_hec_token")
    helper.log_info("puppet_action_hec_token={}".format(puppet_action_hec_token))


    # The following example adds two sample events ("hello", "world")
    # and writes them to Splunk
    # NOTE: Call helper.writeevents() only once after all events
    # have been added
    helper.addevent("hello", sourcetype="sample_sourcetype")
    helper.addevent("world", sourcetype="sample_sourcetype")
    helper.writeevents(index="summary", host="localhost", source="localhost")

    # The following example gets the events that trigger the alert
    events = helper.get_events()
    for event in events:
        helper.log_info("event={}".format(event))

    # helper.settings is a dict that includes environment configuration
    # Example usage: helper.settings["server_uri"]
    helper.log_info("server_uri={}".format(helper.settings["server_uri"]))
    [sample_code_macro:end]
    """
    helper.set_log_level(helper.log_level)

    helper.log_info("Alert action puppet_run_task started.")

    helper.log_info("Log_level: {}".format(helper.log_level))

    # users can provide 3 different usernames:
    # puppet_default_user in the top level config
    # bolt_user in the top level config
    # bolt_user in the alert setup itself
    helper.log_info("Credential lookup")
    puppet_default_user = helper.get_global_setting("puppet_default_user")
    bolt_user_name = override('bolt_user', helper)

    # ok at this point we can get the account
    puppet_bolt_user_name = notnone(puppet_default_user, bolt_user_name, helper)

    puppet_bolt_account = helper.get_user_credential(puppet_bolt_user_name)

    puppet_bolt_user = puppet_bolt_account["username"]
    puppet_bolt_user_pass = puppet_bolt_account["password"]

    helper.log_debug("username={}".format(puppet_bolt_user))

    # load the rest of the settings
    helper.log_info("Retrieving settings")
    # Get PE Console, this doesn't set pe_console value, that is from the alert itself
    puppet_enterprise_console = override("puppet_enterprise_console", helper)
    helper.log_debug("puppet_enterprise_console={}".format(puppet_enterprise_console))
    
    # get the URL that we are sending the new event to
    splunk_hec_url = override("splunk_hec_url", helper)
    helper.log_debug("splunk_hec_url={}".format(splunk_hec_url))

    # get the token we are using for the event
    splunk_hec_token = override("splunk_hec_token", helper)
    helper.log_debug("splunk_hec_token={}".format(splunk_hec_token))

    # we like to be chatty about it so we might have a dedicated token
    puppet_action_hec_token = override("puppet_action_hec_token", helper)
    helper.log_debug("puppet_action_hec_token={}".format(puppet_action_hec_token))

    # this is the timeout we use, rarely an issue for pdb lookup
    timeout = override("timeout", helper)
    helper.log_debug("timeout={}".format(timeout))

    # only need the bolt server
    puppet_bolt_server = override("puppet_bolt_server", helper)
    helper.log_debug("puppet_bolt_server={}".format(puppet_bolt_server))

    # we need a pe_console server hostname to indicate which pe install this is for
    pe_console = override("pe_console", helper)
    helper.log_debug("pe_console={}".format(pe_console))

    # things that inform our actual bolt task

    bolt_target = helper.get_param("bolt_target")
    helper.log_debug("bolt_target={}".format(bolt_target))

    task_name = helper.get_param("task_name")
    helper.log_debug("task_name={}".format(task_name))

    puppet_environment = helper.get_param("puppet_environment")
    helper.log_debug("puppet_environment={}".format(puppet_environment))

    raw_task_parameters = helper.get_param("task_parameters")
    helper.log_debug("raw_task_parameters={}".format(raw_task_parameters))

    helper.log_debug("Validating if user provided Task Parameters are valid json")
    if raw_task_parameters is not None and raw_task_parameters is not '':
        try:
            json_task_parameters = json.loads(raw_task_parameters)
            task_parameters = json.dumps(json_task_parameters)
            helper.log_debug("Task Parameters are valid json")
        except:
            error_string = 'Task {} for host {} uninstigated - Task Parameters must be in a correct JSON format, please check this and try again'.format(task_name,bolt_target)
            helper.log_error(error_string)
    else:
        empty_dict = {}
        task_parameters = json.dumps(empty_dict)
        helper.log_debug("Task Parameters were empty so forcing valid blank json")
    
    helper.log_debug("task_parameters={}".format(task_parameters))

    # create our alert object to build the actual report
    helper.log_info("Assembling alert data")
    alert = {}
    alert['global'] = {}
    alert['param'] = {}
    alert['global']['puppet_enterprise_console'] = puppet_enterprise_console
    alert['global']['splunk_hec_url'] = splunk_hec_url
    alert['global']['bolt_user'] = puppet_bolt_user
    alert['global']['bolt_user_pass'] = puppet_bolt_user_pass
    alert['global']['puppet_bolt_server'] = notnone(puppet_enterprise_console, puppet_bolt_server, helper)
    alert['global']['puppet_action_hec_token'] = notnone(splunk_hec_token, puppet_action_hec_token, helper)
    alert['global']['timeout'] = timeout

    # Load the alert specific settings that are really the task we're running
    alert['param']['bolt_target'] = bolt_target
    alert['param']['task_name'] = task_name
    alert['param']['task_parameters'] = task_parameters
    alert['param']['puppet_environment'] = puppet_environment


    # we don't need to log the event data, but we could do something here to extract if it's a puppet sourcetyep
    # if so, we extract the transaction_uuid to link it back in the action?
    # events = helper.get_events()

    helper.log_info("Alert action data extracted and passed to run_bolt_task")

    run_bolt_task(alert, helper)

    helper.log_info("Bolt task has completed successfully")

    # TODO: Implement your alert action logic here
    return 0
