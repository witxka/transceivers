#!/bin/sh
cp transceivers.py ~/local/lib/check_mk/base/plugins/agent_based/
# commented out due to the security permissions in docker installation
  #cp transceiver_parameter.py ~/lib/check_mk/gui/plugins/wato/check_parameters/
cp package-info.py ~/var/check_mk/packages/transceivers
cp agent/transceivers ~/local/share/check_mk/agents/plugins
