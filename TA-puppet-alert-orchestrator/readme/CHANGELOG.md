# Release Notes

## Version 1.0.0

**Breaking Changes**:

  * This release of the Puppet Alert Orchestrator add-on for Splunk no longer utilizes Splunk's Python2 SDK. As such this version will only work on Splunk Enterprise 8.x+ and Splunk Cloud.
  * Removed a number of "Add-on settings" that were already configurable within the actions.
  * "Run a Bolt Task" is now "Run a Puppet Task".

**New Features**:

  * **Orchestrator Actions**:
    * All new dashboard powered by a custom input which uses the configured account credentials to query PE for Plans and Tasks available to that particular RBAC user.
      * By default the custom input script only checks for actions available in the `production` environment.
  * Added "Run a Puppet Plan" **Action**.
    * New action added that allows user to trigger Puppet Plans. When configuring the action, the Plan name is populated with the same data as the Orchestrator Actions dashboard.
  * "Run a Puppet Task" **Action**.
    *  When configuring the action, the Task name is populated with the same data as the Orchestrator Actions dashboard.

## Version 0.6.0

**Fixes**:

  * In a distributed Splunk installation, settings specific to this add-on were not properly replicated across the cluster. This release adds a default `server.conf` file with an `[shclustering]` stanza to ensure the proper settings are replicated.

## Version 0.5.0

**Notes**:

  * This is an initial release of the Puppet Alert Actions App. This contains just the alert actions needed to retrieve detailed reports or run tasks in Puppet Enterprise. This App is only for Puppet Enterprise users.
