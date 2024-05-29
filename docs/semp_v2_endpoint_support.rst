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
   * - "/SEMP/v2/config/about"
     - GET
     - False
     - Not supporting because it gives same info as "/SEMP/v2/config/about/api" but has a less specific name.
   * - "/SEMP/v2/config/about/api"
     - GET
     - True
     - 
   * - "/SEMP/v2/config/about/user"
     - GET
     - Pending
     - 
   * - "/SEMP/v2/config/about/user/msgVpns"
     - GET
     - Pending
     -  
   * - "/SEMP/v2/config/about/user/msgVpns/{msgVpnName}"
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
   * - "/SEMP/v2/config/clientCertAuthorities"
     - GET
     - Pending
     - 
   * - "/SEMP/v2/config/clientCertAuthorities"
     - POST
     - Pending
     - 
   * - "/SEMP/v2/config/clientCertAuthorities/{certAuthorityName}"
     - DELETE
     - Pending
     - 
   * - "/SEMP/v2/config/clientCertAuthorities/{certAuthorityName}"
     - GET
     - Pending
     -  
   * - "/SEMP/v2/config/clientCertAuthorities/{certAuthorityName}"
     - PATCH
     - Pending
     - 
   * - "/SEMP/v2/config/clientCertAuthorities/{certAuthorityName}"
     - PUT
     - Pending
     - 
   * - "/SEMP/v2/config/clientCertAuthorities/{certAuthorityName}/ocspTlsTrustedCommonNames"
     - GET
     - Pending
     - 
   * - "/SEMP/v2/config/clientCertAuthorities/{certAuthorityName}/ocspTlsTrustedCommonNames"
     - POST
     - Pending
     - 
   * - "/SEMP/v2/config/clientCertAuthorities/{certAuthorityName}/ocspTlsTrustedCommonNames/{ocspTlsTrustedCommonName}"
     - DELETE
     - Pending
     - 
   * - "/SEMP/v2/config/clientCertAuthorities/{certAuthorityName}/ocspTlsTrustedCommonNames/{ocspTlsTrustedCommonName}"
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
   * - "/SEMP/v2/config/msgVpns"
     - GET
     - True
     - 
   * - "/SEMP/v2/config/msgVpns"
     - POST
     - True
     - 
   * - "/SEMP/v2/config/msgVpns/{msgVpnName}"
     - DELETE
     - True
     - 
   * - "/SEMP/v2/config/msgVpns/{msgVpnName}"
     - GET
     - Pending
     - 
   * - "/SEMP/v2/config/msgVpns/{msgVpnName}"
     - PATCH
     - Pending
     - 
   * - "/SEMP/v2/config/msgVpns/{msgVpnName}"
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

> clientProfile (Table Pending)

> clientUsername (Table Pending)

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