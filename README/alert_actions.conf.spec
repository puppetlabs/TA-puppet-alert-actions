
[puppet_generate_detailed_report]
python.version = python3
param.puppet_enterprise_console = <string> Puppet Enterprise Console.
param.puppet_default_user = <string> User.
param.splunk_hec_url = <string> Splunk HEC URL.
param.splunk_hec_token = <string> Splunk HEC Token.
param.puppet_action_hec_token = <string> Action HEC Token.
param.puppet_db_url = <string> PuppetDB URL.
param.timeout = <string> Timeout.

[puppet_run_task]
python.version = python3
param.bolt_target = <string> Host. It's a required parameter. It's default value is $result.host$.
param.task_name = <string> Task. It's a required parameter.
param.task_parameters = <string> Task Parameters.
param.puppet_environment = <string> Puppet Environment. It's a required parameter. It's default value is production.
param.puppet_enterprise_console = <string> Puppet Enterprise Console.
param.puppet_bolt_server = <string> Orch. Services URL.
param.puppet_db_url = <string> PuppetDB URL.
param.timeout = <string> Timeout.
param.splunk_hec_url = <string> Splunk HEC URL.
param.puppet_action_hec_token = <string> Action HEC Token.

