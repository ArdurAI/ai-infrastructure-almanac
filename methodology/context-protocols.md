# Context & Protocols — Testing Methodology

How we test and score AI protocols, authentication standards, and integration patterns in the almanac.

## Scope

This category covers communication protocols (MCP, A2A), authentication standards (OAuth 2.1, WIMSE, AIMS), and gateway/registry infrastructure that enables AI agent interoperability.

## Adapter pattern

```python
class ProtocolAdapter(CategoryAdapter):
    def setup(self, config) -> None:
        # Deploy protocol server or SDK, configure endpoints
        pass
    
    def load(self, capabilities) -> None:
        # Register tools, agents, or services with the protocol
        pass
    
    def query(self, request) -> Response:
        # Send a protocol request, return response + latency
        pass
    
    def teardown(self) -> None:
        # Deregister, stop server, clean connections
        pass
```

## Standard benchmarks

### 1. Protocol compliance
- **What**: Run the official protocol test suite (if available)
- **Why**: Ensures interoperability with other implementations
- **Metric**: Pass rate on compliance tests, spec version adherence

### 2. Authentication robustness
- **What**: Test auth flows (OAuth 2.1, PKCE, WIMSE, agent assertions)
- **Why**: Security is critical for agent-to-agent communication
- **Metric**: Token handling, refresh logic, scope enforcement, revocation

### 3. Interoperability
- **What**: Connect implementation A to implementation B from different vendors
- **Why**: Protocols are only useful if they work across vendors
- **Metric**: Connection success rate, feature negotiation, error handling

## Custom PlatformOps benchmarks

### Connection latency
- **Tasks**: Establish 1000 protocol connections
- **Metrics**: Handshake time, connection setup latency, TLS overhead

### Throughput
- **Tasks**: Exchange 10K messages via the protocol
- **Metrics**: Messages/second, payload size scaling, batching support

### Security scanning
- **Tasks**: Run 50 security tests (MITM, replay, token forgery, scope escalation)
- **Metrics**: Vulnerability count, severity, remediation guidance

### Registry/discovery
- **Tasks**: Register and discover 100 services via the protocol registry
- **Metrics**: Discovery latency, search accuracy, metadata completeness

### Gateway performance
- **Tasks**: Route 10K requests through an AI gateway
- **Metrics**: Routing latency, fallback behavior, circuit breaker response

## Scoring dimensions

| Dimension | Weight | How measured |
|-----------|--------|-------------|
| **Accuracy** | 25% | Protocol compliance, interoperability success rate, spec adherence |
| **Latency** | 20% | Connection setup, message round-trip, discovery latency |
| **Token economics** | 10% | Overhead per message, payload efficiency, batching support |
| **Scale behavior** | 15% | Performance at 100, 1000, 10000 concurrent connections |
| **Ops burden** | 15% | Deployment complexity, certificate management, rotation workflow |
| **Developer experience** | 10% | SDK quality, documentation, error messages, debugging tools |
| **Data sovereignty** | 5% | Self-hosted registry, local protocol enforcement, audit logs |

## Stress suites

### Contradiction storm
- Two services with conflicting capability declarations
- Measure: Resolution strategy, error handling, user feedback

### Near-duplicate flood
- 1000 services with nearly identical names/capabilities
- Measure: Discovery accuracy, deduplication, search relevance

### Temporal paradox
- Token expires mid-conversation; refresh token also expired
- Measure: Graceful degradation, re-auth flow, session recovery

### Concurrent writers
- 100 clients registering services simultaneously
- Measure: Race conditions, consistency, duplicate handling

### Kill-the-backing-store
- Kill the registry or authentication server mid-request
- Measure: Fallback behavior, cached credentials, offline operation

## Known pitfalls

1. **Spec drift**: Implementations claim compliance but don't actually follow the spec. We test against reference implementations.
2. **Security theater**: "Enterprise-grade security" claims without actual testing. We run penetration tests.
3. **Version fragmentation**: Protocol v1 vs v2 incompatibility. We test version negotiation.
4. **MCP auth gap**: As noted in June 2026, 100% of scanned MCP servers lacked auth. We test auth requirements.

## License
Content is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / AI Infrastructure Almanac**.
