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
     - Pending
     - 
   * - "/about/user/msgVpns"
     - GET
     - Pending
     -  
   * - "/about/user/msgVpns/{msgVpnName}"
     - GET
     - Pending
     -  


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

.. list-table:: Category: clientCertAuthority (Table unfinished)
   :widths: 30 5 5 15
   :header-rows: 1

   * - Endpoint
     - Method
     - Supported
     - Info
   * - "/msgVpns"
     - GET
     - True
     - 
   * - "/msgVpns"
     - POST
     - True
     - 
   * - "/msgVpns/{msgVpnName}"
     - DELETE
     - True
     - 
   * - "/msgVpns/{msgVpnName}"
     - GET
     - Pending
     - 
   * - "/msgVpns/{msgVpnName}"
     - PATCH
     - Pending
     - 
   * - "/msgVpns/{msgVpnName}"
     - PUT
     - True
     - 

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