# Authentication & Identity for AI

> **Cross-cutting concern.** Authentication and identity for AI agents are currently tracked within the [Context Protocols](../context-protocols/) category, as they are inseparable from the protocol layer (MCP, A2A, OAuth 2.1, WIMSE, AIMS). This dedicated directory will be populated if the category grows large enough to warrant a split in a future edition.

## Key Tools (in Context Protocols)

| Tool | Type | Focus |
|------|------|-------|
| OAuth 2.1 + PKCE | Auth Standard | Dominant pattern for AI agent authentication |
| WIMSE (IETF) | Standard | Workload identity; SPIFFE successor |
| AIMS (IETF) | Standard | AI agent auth/authz; `agent_assertion` grant type |
| SCIM for Agents | Standard | Agent lifecycle management |
| Authed | Auth Protocol | Unique agent IDs, dynamic tokens, registry |
| HashiCorp Vault | Secrets Mgmt | Enterprise standard; dynamic secrets |
| AWS Secrets Manager | Secrets Mgmt | AWS-native; automated rotation |
| Stytch | Auth Platform | Connected Apps; MCP auth server |
| Scalekit | Auth Platform | OAuth for AI agents; delegated auth |
| Aembit | Auth Platform | MCP authorization; workload identity |
| Trulioo KYA | Trust | Digital Agent Passports; Know Your Agent |
| Visa TAP | Trust | Trusted Agent Protocol |

## See also

- Full context protocols catalog: [`../context-protocols/README.md`](../context-protocols/README.md)
- Latest edition: [`../editions/2026-06.md`](../editions/2026-06.md)
