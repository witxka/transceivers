# transceivers

Optical transceivers plugin for check_mk 2 through ethtool.

Plugin consist of:
  * mkp plugin with agent setup for some mellanox 100Gbs transceiver parameters

All optical transceiver parameters presented with csv files.
Due to security permissions in check_mk docker installation rule definition must be copied manually
to the check_mk:
  * cp transceiver_parameter.py ~/lib/check_mk/gui/plugins/wato/check_parameters/
  * omd restart apache
