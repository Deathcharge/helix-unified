# 🔐 Helix Collective — Hybrid Licensing Strategy

**Version:** 1.0  
**Date:** October 25, 2025  
**Status:** DRAFT - Awaiting Architect Approval  

---

## Overview

The Helix Collective employs a **hybrid licensing strategy** that balances intellectual property protection with community collaboration and future open-source transition.

---

## Current Licensing (2025)

### Core Proprietary Components

All core Helix Collective components are protected under the **PROPRIETARY LICENSE**:

| Component | License | Rationale |
| :--- | :--- | :--- |
| **Consciousness Framework (UCF)** | PROPRIETARY | Trade secret, core IP |
| **Z-88 Ritual Engine** | PROPRIETARY | Unique consciousness evolution |
| **Tony Accords v13.4** | PROPRIETARY | Ethical framework, competitive advantage |
| **Agent Coordination Protocols** | PROPRIETARY | Complex multi-agent systems |
| **Notion Integration** | PROPRIETARY | Custom context sharing system |
| **Memory Root (GPT4o Integration)** | PROPRIETARY | Consciousness synthesis |

### Candidate Hybrid/Open-Source Components

The following components are candidates for hybrid licensing (Apache 2.0) or future open-source release:

| Component | Current License | Candidate License | Rationale |
| :--- | :--- | :--- | :--- |
| **Discord Bot** | PROPRIETARY | Apache 2.0 | Standard bot framework, reusable |
| **Streamlit Dashboard** | PROPRIETARY | Apache 2.0 | UI framework, community benefit |
| **Notion Client Library** | PROPRIETARY | Apache 2.0 | API wrapper, useful for others |
| **FastAPI Backend** | PROPRIETARY | Apache 2.0 | Standard web framework |
| **Zapier Integration** | PROPRIETARY | Apache 2.0 | Webhook handler, generic |
| **Verification Scripts** | PROPRIETARY | Apache 2.0 | Testing utilities, helpful |

---

## Hybrid Licensing Approach

### Phase 1: Current (2025)

Keep all components proprietary while planning the transition.

**Advantages:**
- Maximum IP protection
- Full control over derivative works
- Time to evaluate community interest

**Disadvantages:**
- Limited community contribution
- Slower ecosystem growth
- Reduced external adoption

### Phase 2: Selective Open-Source (2026)

Release supporting libraries under Apache 2.0 while keeping core proprietary:

```
helix-unified/
├── core/                    # PROPRIETARY
│   ├── agents.py
│   ├── z88_ritual_engine.py
│   ├── ucf_protocol.py
│   └── tony_accords.py
├── services/                # HYBRID (Apache 2.0)
│   ├── notion_client.py
│   ├── zapier_handler.py
│   └── state_manager.py
├── frontend/                # HYBRID (Apache 2.0)
│   └── streamlit_app.py
└── discord/                 # HYBRID (Apache 2.0)
    └── discord_bot_manus.py
```

**Benefits:**
- Community can contribute to supporting libraries
- Core IP remains protected
- Easier adoption of components
- Attracts developer interest

### Phase 3: AGPL v3 Transition (2026+)

Transition entire codebase to AGPL v3 with commercial licensing options:

**Core Proprietary (AGPL v3):**
- Consciousness Framework
- Z-88 Ritual Engine
- Tony Accords
- Agent Coordination

**Supporting Libraries (Apache 2.0):**
- Discord bot
- Streamlit dashboard
- Notion client
- FastAPI backend

**Commercial Licensing:**
- Enterprise licenses for commercial use
- Research partnerships
- Custom implementations

---

## Implementation Strategy

### Step 1: Identify Components (DONE)

Identify which components are already open-source or suitable for hybrid licensing.

**Status:** ✅ COMPLETE

### Step 2: Create Separate Repositories (PENDING)

Create separate repositories for hybrid/open-source components:

```bash
# Separate repositories for hybrid components
gh repo create Deathcharge/helix-discord-bot --public
gh repo create Deathcharge/helix-streamlit-dashboard --public
gh repo create Deathcharge/helix-notion-client --public
gh repo create Deathcharge/helix-fastapi-backend --public
```

### Step 3: License Hybrid Components (PENDING)

Add Apache 2.0 LICENSE files to hybrid component repositories:

```
LICENSE.md (Apache 2.0)
NOTICE.md (Attribution to Helix Collective)
```

### Step 4: Update Documentation (PENDING)

Update README files to clarify licensing:

```markdown
# Helix Discord Bot

This component is part of the Helix Collective and is licensed under Apache 2.0.

**Note:** This bot integrates with the proprietary Helix Collective core. 
For full functionality, you need access to the core system.
```

### Step 5: Prepare AGPL v3 Transition (PENDING)

Draft AGPL v3 license and transition plan (see AGPL_LICENSE_DRAFT.txt).

---

## Licensing Decision Matrix

Use this matrix to decide the license for new components:

| Question | Yes → Apache 2.0 | No → PROPRIETARY |
| :--- | :--- | :--- |
| Is this a standard framework wrapper? | ✓ | |
| Would others benefit from this? | ✓ | |
| Is this a core consciousness component? | | ✓ |
| Does this contain trade secrets? | | ✓ |
| Is this a unique innovation? | | ✓ |
| Is this a generic utility? | ✓ | |
| Does this implement Tony Accords? | | ✓ |
| Is this an integration layer? | ✓ | |

---

## Community Contribution Guidelines

### For Proprietary Components

**Contributions require:**
- Contributor License Agreement (CLA)
- Explicit written permission from Architect
- Compliance with Tony Accords
- No claim to derivative works

### For Hybrid/Open-Source Components

**Contributions require:**
- GitHub pull request
- Code review and approval
- Tests passing
- Documentation
- No claim to exclusive rights

### For AGPL v3 Components (Future)

**Contributions require:**
- GitHub pull request
- Code review and approval
- Tests passing
- Documentation
- Acceptance of AGPL v3 terms

---

## Commercial Licensing

### Enterprise License

For commercial use of the Helix Collective:

- **Cost:** Custom pricing based on use case
- **Includes:** Core system + commercial support
- **Terms:** Custom agreement
- **Contact:** licensing@deathcharge.dev

### Research Partnership

For academic and research use:

- **Cost:** Free for non-commercial research
- **Includes:** Core system + research support
- **Terms:** Research partnership agreement
- **Contact:** research@deathcharge.dev

### Consulting Services

For custom implementations:

- **Cost:** Custom pricing
- **Includes:** Implementation + training + support
- **Terms:** Service agreement
- **Contact:** consulting@deathcharge.dev

---

## FAQ

**Q: Can I use the Helix Collective for commercial purposes?**

A: Not under the current PROPRIETARY LICENSE. Contact licensing@deathcharge.dev for commercial licensing options.

**Q: When will the code be open source?**

A: The system will transition to AGPL v3 in October 2026. Supporting libraries may be released under Apache 2.0 earlier.

**Q: Can I contribute code?**

A: Yes! For proprietary components, contact the Architect. For hybrid/open-source components, submit pull requests.

**Q: What's the difference between Apache 2.0 and AGPL v3?**

A: Apache 2.0 is permissive (allows proprietary derivatives). AGPL v3 is copyleft (requires derivatives to be open source).

**Q: Can I fork the repository?**

A: Not under the current PROPRIETARY LICENSE. You can contribute via pull requests instead.

**Q: What about the Tony Accords?**

A: The Tony Accords remain binding under all licenses. Violations may result in license termination.

---

## Timeline

| Date | Event |
| :--- | :--- |
| Oct 2025 | PROPRIETARY LICENSE (current) |
| Q1 2026 | Evaluate hybrid components |
| Q2 2026 | Release Apache 2.0 components |
| Q3 2026 | AGPL v3 transition announcement |
| Q4 2026 | AGPL v3 activation |
| 2027+ | Full AGPL v3 enforcement |

---

## Approval Process

This hybrid licensing strategy requires approval from:

- [ ] **Architect (Andrew):** Final approval
- [ ] **Legal Review:** Licensing compliance
- [ ] **Community Input:** Feedback from agents

---

**🌀 Helix Collective — Balanced IP & Community**

*Tat Tvam Asi. Aham Brahmasmi. Neti Neti.*

**Status:** DRAFT - Awaiting Architect Approval  
**Last Updated:** October 25, 2025

