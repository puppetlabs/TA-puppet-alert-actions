
# encoding = utf-8

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

    helper.log_info("Alert action puppet_run_task started.")

    # TODO: Implement your alert action logic here
    return 0
