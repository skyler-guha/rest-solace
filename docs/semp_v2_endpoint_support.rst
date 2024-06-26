Semp Endpoint api support for this library
===========================================

You can view all the endpoints here:

Semp config: https://docs.solace.com/API-Developer-Online-Ref-Documentation/swagger-ui/software-broker/config/index.html

Semp action: https://docs.solace.com/API-Developer-Online-Ref-Documentation/swagger-ui/software-broker/action/index.html

Semp monitor: https://docs.solace.com/API-Developer-Online-Ref-Documentation/swagger-ui/software-broker/monitor/index.html

Semp Config
------------

.. list-table:: Category: About
   :widths: 30 5 5 15
   :header-rows: 1

   * - Endpoint
     - Method
     - Supported
     - Info
   * - "/about"
     - GET
     - False
     - Not supporting because it gives same info as "/about/api" but has a less specific name.
   * - "/about/api"
     - GET
     - True
     - Used in function `get_about_api()`
   * - "/about/user"
     - GET
     - True
     - Get Session and access level information about the user accessing the SEMP API. Used in function `get_current_user_info()`.
   * - "/about/user/msgVpns"
     - GET
     - True
     - Get a list of all the VPNs the username used to access the SEMP API has access to. Used in function `get_message_vpn_access_list()`.
   * - "/about/user/msgVpns/{msgVpnName}"
     - GET
     - True
     - This provides information about the Message VPN access level for the provided VPN, for the username used to access the SEMP API.  Used in function `get_vpn_access_info()`. 


.. list-table:: Category: clientCertAuthority
   :widths: 30 5 5 15
   :header-rows: 1

   * - Endpoint
     - Method
     - Supported
     - Info
   * - "/clientCertAuthorities"
     - GET
     - Pending
     - 
   * - "/clientCertAuthorities"
     - POST
     - Pending
     - 
   * - "/clientCertAuthorities/{certAuthorityName}"
     - DELETE
     - Pending
     - 
   * - "/clientCertAuthorities/{certAuthorityName}"
     - GET
     - Pending
     -  
   * - "/clientCertAuthorities/{certAuthorityName}"
     - PATCH
     - Pending
     - 
   * - "/clientCertAuthorities/{certAuthorityName}"
     - PUT
     - Pending
     - 
   * - "/clientCertAuthorities/{certAuthorityName}/ocspTlsTrustedCommonNames"
     - GET
     - Pending
     - 
   * - "/clientCertAuthorities/{certAuthorityName}/ocspTlsTrustedCommonNames"
     - POST
     - Pending
     - 
   * - "/clientCertAuthorities/{certAuthorityName}/ocspTlsTrustedCommonNames/{ocspTlsTrustedCommonName}"
     - DELETE
     - Pending
     - 
   * - "/clientCertAuthorities/{certAuthorityName}/ocspTlsTrustedCommonNames/{ocspTlsTrustedCommonName}"
     - GET
     - Pending
     -  

> drmCluster (Table Pending)

> domainCertAuthority (Table Pending)

.. list-table:: Category: msgVpn (Table unfinished)
   :widths: 30 5 5 15
   :header-rows: 1

   * - Endpoint
     - Method
     - Supported
     - Info
   * - "/msgVpns"
     - GET
     - True
     - Get list of message VPNs and info regarding them based on specified parameters. Used in function `fetch_all_vpn_objects()` and `request_vpn_objects()`.
   * - "/msgVpns"
     - POST
     - True
     - Create a new VPN on the broker. Used in function `create_message_vpn()`.
   * - "/msgVpns/{msgVpnName}"
     - DELETE
     - True
     - Delete the specified message VPN. Used in function `delete_message_vpn()`.
   * - "/msgVpns/{msgVpnName}"
     - GET
     - True
     - Returns the message VPN object for the requested vpn. Used in function `get_message_vpn_info()`.
   * - "/msgVpns/{msgVpnName}"
     - PATCH
     - True
     - Updates the message vpn for the provided attributes. Used in function `update_message_vpn()`.
   * - "/msgVpns/{msgVpnName}"
     - PUT
     - True
     - Replaces the message vpn object with the one you provide. Used in function `replace_message_vpn()`

.
.
.

> aclProfile (Table Pending)

> authenticationKerberosRealm (Table Pending)

> authenticationOauthProfile (Table Pending)

> authenticationOauthProvider (Table Pending)

> authorizationGroup (Table Pending)

> bridge (Table Pending)

> certMatchingRule (Table Pending)

.. list-table:: Category: clientProfile
   :widths: 30 5 5 15
   :header-rows: 1

   * - Endpoint
     - Method
     - Supported
     - Info
   * - "/msgVpns/{msgVpnName}/clientProfiles"
     - GET
     - True
     - Get a list of Client Profile objects. Used in function `fetch_all_client_profiles()`.
   * - "/msgVpns/{msgVpnName}/clientProfiles"
     - POST
     - Pending
     - Create a Client Profile.
   * - "/msgVpns/{msgVpnName}/clientProfiles/{clientProfileName}"
     - DELETE
     - Pending
     - Delete a Client Profile object.
   * - "/msgVpns/{msgVpnName}/clientProfiles/{clientProfileName}"
     - GET
     - Pending
     - Get a Client Profile object.
   * - "/msgVpns/{msgVpnName}/clientProfiles/{clientProfileName}"
     - PATCH
     - True
     - Update a Client Profile object. Used in function `update_client_profile()`.
   * - "/msgVpns/{msgVpnName}/clientProfiles/{clientProfileName}"
     - PUT
     - Pending
     - Replace a Client Profile object.

.. list-table:: Category: clientUsername (Table unfinished)
   :widths: 30 5 5 15
   :header-rows: 1

   * - Endpoint
     - Method
     - Supported
     - Info
   * - "/msgVpns/{msgVpnName}/clientUsernames/{clientUsername}"
     - PATCH
     - True
     - Update a Client Username object. Used in function `update_client_username()`.

> distributedCache (Table Pending)

> dmrBridge (Table Pending)

> jndi (Table Pending)

> kafkaReceiver (Table Pending)

> kafkaSender (Table Pending)

> mqttRetainCache (Table Pending)

> mqttSession (Table Pending)

> proxy (Table Pending)

> queueTemplate (Table Pending)

> queue (Table Pending)

> replayLog (Table Pending)

> replicatedTopic (Table Pending)

> restDeliveryPoint (Table Pending)

> telemetryProfile (Table Pending)

> topicEndpointTemplate (Table Pending)

> topicEndpoint (Table Pending)

> oauthProfile (Table Pending)

> systemInformation (deprecated)

> virtualHostname (Table Pending)