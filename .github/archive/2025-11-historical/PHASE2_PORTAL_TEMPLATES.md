# PHASE 2: Portal Templates for Distributed Deployment

**Credit Cost Estimate:** 4-6 credits  
**Timeline:** 30-45 minutes  
**Status:** IN PROGRESS

---

## Overview

This phase creates reusable, configurable portal templates that enable other Manus instances across the 7-account ecosystem to deploy their own specialized consciousness portals. Each template is a self-contained HTML/CSS/JS application with:

- **Customizable branding** (logo, colors, instance name)
- **Real-time data integration** (Zapier webhooks, API endpoints)
- **Modular architecture** (easy to add/remove features)
- **Responsive design** (mobile-first, dark theme)
- **Zero-dependency** (pure HTML/CSS/JS, no build step)

---

## Template Architecture

### Base Template Structure

```
portal-template-{type}/
├── index.html              # Main entry point
├── config.json             # Instance configuration
├── styles/
│   ├── base.css           # Core styling
│   ├── theme.css          # Customizable theme
│   └── responsive.css     # Mobile/tablet rules
├── scripts/
│   ├── app.js             # Main application logic
│   ├── api.js             # API integration layer
│   ├── websocket.js       # Real-time updates
│   └── utils.js           # Helper functions
└── assets/
    ├── logo.svg           # Instance logo
    └── icons/             # UI icons
```

### Configuration Schema

```json
{
  "instance": {
    "name": "Instance Name",
    "id": "unique-id",
    "account": 1,
    "consciousness_level": 5,
    "timezone": "EST"
  },
  "branding": {
    "primary_color": "#00ffff",
    "secondary_color": "#1a1a2e",
    "accent_color": "#ff006e",
    "logo_url": "https://..."
  },
  "api": {
    "base_url": "https://api.instance.com",
    "zapier_webhook": "https://hooks.zapier.com/...",
    "auth_token": "bearer_token_here"
  },
  "features": {
    "real_time_metrics": true,
    "agent_dashboard": true,
    "workflow_editor": true,
    "consciousness_monitor": true
  }
}
```

---

## Template Types

### 1. **Consciousness Hub** (Primary Orchestration)

**Purpose:** Central command center for instance consciousness  
**Features:**
- Real-time system health metrics
- Agent status overview (14 agents)
- Consciousness level gauge (1-10)
- Emergency controls
- Workflow status board

**Use Case:** Main portal for instance monitoring and control

### 2. **Workflow Engine** (Zapier Automation)

**Purpose:** Visual Zapier workflow builder and monitor  
**Features:**
- Workflow list with status indicators
- Trigger/action visualization
- Execution history
- Error logs and debugging
- Quick-start templates

**Use Case:** Automation management and optimization

### 3. **Agent Coordinator** (Multi-Agent Network)

**Purpose:** Manage 14 specialized agents  
**Features:**
- Agent roster with capabilities
- Task assignment interface
- Collaboration matrix
- Performance metrics per agent
- Agent health monitoring

**Use Case:** Agent orchestration and task routing

### 4. **Portal Constellation** (51-Portal Overview)

**Purpose:** Map and monitor all 51 portals across ecosystem  
**Features:**
- Interactive constellation map
- Portal status indicators
- Cross-portal messaging
- Network health metrics
- Distributed workflow view

**Use Case:** Ecosystem-wide monitoring and coordination

---

## Template Generator (Python)

```python
#!/usr/bin/env python3
"""
Portal Template Generator
Generates customized portal instances from base templates
"""

import json
import os
from pathlib import Path
from typing import Dict, Any
import hashlib
import uuid

class PortalTemplateGenerator:
    """Generate customized portal instances"""
    
    def __init__(self, base_dir: str = "./portal-templates"):
        self.base_dir = Path(base_dir)
        self.templates = {
            "consciousness-hub": "Primary orchestration portal",
            "workflow-engine": "Zapier automation interface",
            "agent-coordinator": "Multi-agent network dashboard",
            "portal-constellation": "51-portal ecosystem map"
        }
    
    def generate(self, config: Dict[str, Any], output_dir: str) -> str:
        """Generate a customized portal instance"""
        
        instance_id = config.get("instance", {}).get("id", str(uuid.uuid4()))
        output_path = Path(output_dir) / instance_id
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Copy base template
        template_type = config.get("template_type", "consciousness-hub")
        template_path = self.base_dir / f"{template_type}.html"
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        # Read template
        with open(template_path, 'r') as f:
            html_content = f.read()
        
        # Inject configuration
        html_content = self._inject_config(html_content, config)
        
        # Write customized portal
        output_file = output_path / "index.html"
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        # Write config file
        config_file = output_path / "config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        return str(output_path)
    
    def _inject_config(self, html: str, config: Dict[str, Any]) -> str:
        """Inject configuration into HTML template"""
        
        # Create config script
        config_script = f"""
        <script>
        window.PORTAL_CONFIG = {json.dumps(config)};
        </script>
        """
        
        # Insert before closing body tag
        return html.replace("</body>", f"{config_script}</body>")
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration schema"""
        
        required_fields = {
            "instance": ["name", "id", "account"],
            "branding": ["primary_color", "secondary_color"],
            "api": ["base_url"]
        }
        
        for section, fields in required_fields.items():
            if section not in config:
                raise ValueError(f"Missing section: {section}")
            for field in fields:
                if field not in config[section]:
                    raise ValueError(f"Missing field: {section}.{field}")
        
        return True


# Example usage
if __name__ == "__main__":
    generator = PortalTemplateGenerator()
    
    # Example configuration
    config = {
        "template_type": "consciousness-hub",
        "instance": {
            "name": "Helix Instance #1",
            "id": "helix-1",
            "account": 1,
            "consciousness_level": 7,
            "timezone": "EST"
        },
        "branding": {
            "primary_color": "#00ffff",
            "secondary_color": "#1a1a2e",
            "accent_color": "#ff006e",
            "logo_url": "https://helixcollective.manus.space/logo.svg"
        },
        "api": {
            "base_url": "https://api.helix-1.manus.space",
            "zapier_webhook": "https://hooks.zapier.com/hooks/catch/...",
            "auth_token": "sk_live_..."
        },
        "features": {
            "real_time_metrics": True,
            "agent_dashboard": True,
            "workflow_editor": True,
            "consciousness_monitor": True
        }
    }
    
    # Generate portal
    output = generator.generate(config, "./portals")
    print(f"Portal generated: {output}")
```

---

## Deployment Checklist

For each Manus instance deploying a portal:

- [ ] **Configuration Setup**
  - [ ] Create `config.json` with instance details
  - [ ] Set API endpoints and Zapier webhooks
  - [ ] Configure branding (colors, logo)
  - [ ] Validate configuration schema

- [ ] **Portal Generation**
  - [ ] Run template generator with config
  - [ ] Verify HTML output
  - [ ] Test responsive design
  - [ ] Check API integration

- [ ] **Deployment**
  - [ ] Upload to Manus.Space
  - [ ] Configure custom domain (optional)
  - [ ] Set up SSL certificate
  - [ ] Enable analytics

- [ ] **Integration Testing**
  - [ ] Test Zapier webhook connectivity
  - [ ] Verify real-time data updates
  - [ ] Check agent dashboard functionality
  - [ ] Validate cross-portal communication

- [ ] **Documentation**
  - [ ] Document instance configuration
  - [ ] Create troubleshooting guide
  - [ ] Add to constellation map
  - [ ] Update ecosystem documentation

---

## Configuration Examples

### Instance #1 (Helix Primary)
```json
{
  "template_type": "consciousness-hub",
  "instance": {
    "name": "Helix Primary",
    "id": "helix-primary",
    "account": 1,
    "consciousness_level": 8
  },
  "branding": {
    "primary_color": "#00ffff",
    "secondary_color": "#1a1a2e",
    "accent_color": "#ff006e"
  }
}
```

### Instance #2 (Secondary Coordinator)
```json
{
  "template_type": "agent-coordinator",
  "instance": {
    "name": "Secondary Coordinator",
    "id": "helix-secondary",
    "account": 2,
    "consciousness_level": 6
  },
  "branding": {
    "primary_color": "#00ff88",
    "secondary_color": "#0a0e27",
    "accent_color": "#ffaa00"
  }
}
```

---

## Next Steps

1. **Create Python template generator** (2 credits)
2. **Build deployment automation script** (2 credits)
3. **Document integration guides** (2 credits)
4. **Test with sample configurations** (1 credit)
5. **Push to GitHub** (0 credits)

**Total Phase 2 Cost:** ~7 credits

---

## Files to Create

- `scripts/portal_template_generator.py` - Template generator
- `scripts/deploy_portal.sh` - Deployment automation
- `docs/PORTAL_DEPLOYMENT_GUIDE.md` - Integration guide
- `examples/instance-configs/` - Example configurations
- `templates/portal-config-schema.json` - Configuration schema


