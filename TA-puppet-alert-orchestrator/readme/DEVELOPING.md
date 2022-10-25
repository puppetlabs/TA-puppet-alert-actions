# Puppet Alert Orchestrator Development Guide

This add-on was originally created using the [Splunk Add-on Builder](https://splunkbase.splunk.com/app/2962) tool within the Splunk UI; while it still utilizes the [`aob_py3` library](https://docs.splunk.com/Documentation/AddonBuilder/latest/UserGuide/PythonHelperFunctions), this add-on can no longer be imported and exported into the Add-on Builder app due to a number of custom changes made to **v1.0.0**.

## Input Scripts

Custom input scripts can be found in `bin/inputs` with configuration located in `default/inputs.conf`.

For detailed information on creating custom inputs, see the Splunk documentation [here](https://dev.splunk.com/enterprise/docs/developapps/manageknowledge/custominputs/scriptedinputsexample/).

## Alert Actions

### Python Code

The following files in `bin/ta_puppet_alert_actions` are modifiable for this add-on:

```
pie/*
modalert_generate_detailed_report_helper.py
modalert_puppet_run_plan_helper.py
modalert_puppet_run_task_helper.py
puppet_plan_action.py
puppet_report_generation.py
puppet_task_action.py
```

The following files are Splunk generated files that should be used as an example when adding new Alert Actions to this add-on:

```
bin/puppet_generate_detailed_report.py
bin/puppet_run_plan.py
bin/puppet_run_task.py
```

### Developing Alert Actions

A single alert action (`puppet_run_plan`) consists of the following files:

  * `bin/puppet_run_plan.py`
  * `bin/ta_puppet_alert_actions/modalert_puppet_run_plan_helper.py`
  * `bin/ta_puppet_alert_actions/puppet_plan_action.py`

While the manual steps are not the exact same, additional information on creating custom alert actions can be found in the Splunk documentation [here](https://docs.splunk.com/Documentation/AddonBuilder/latest/UserGuide/CreateAlertActions).
