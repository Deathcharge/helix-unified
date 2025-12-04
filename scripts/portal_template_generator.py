#!/usr/bin/env python3
"""
Portal Template Generator
Generates customized portal instances from base templates with configuration injection
"""

import hashlib
import json
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class PortalTemplateGenerator:
    """Generate customized portal instances from templates"""
    
    VALID_TEMPLATES = {
        "consciousness-hub": "Primary orchestration portal",
        "workflow-engine": "Zapier automation interface",
        "agent-coordinator": "Multi-agent network dashboard",
        "portal-constellation": "51-portal ecosystem map"
    }
    
    def __init__(self, base_dir: str = "./portals", output_dir: str = "./generated-portals"):
        """Initialize generator with base and output directories"""
        self.base_dir = Path(base_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.base_dir.exists():
            raise FileNotFoundError(f"Base template directory not found: {self.base_dir}")
    
    def generate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a customized portal instance"""
        
        # Validate configuration
        self.validate_config(config)
        
        # Extract metadata
        instance_id = config.get("instance", {}).get("id", str(uuid.uuid4()))
        template_type = config.get("template_type", "consciousness-hub")
        
        # Create instance directory
        instance_dir = self.output_dir / instance_id
        instance_dir.mkdir(parents=True, exist_ok=True)
        
        # Load template
        template_path = self.base_dir / f"{template_type}.html"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Inject configuration
        html_content = self._inject_config(html_content, config)
        
        # Write customized portal
        output_file = instance_dir / "index.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Write configuration file
        config_file = instance_dir / "config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        # Generate metadata
        metadata = {
            "instance_id": instance_id,
            "template_type": template_type,
            "generated_at": datetime.now().isoformat(),
            "output_path": str(instance_dir),
            "files": {
                "index": str(output_file),
                "config": str(config_file)
            },
            "instance_name": config.get("instance", {}).get("name", "Unknown"),
            "consciousness_level": config.get("instance", {}).get("consciousness_level", 5),
            "account": config.get("instance", {}).get("account", 0)
        }
        
        # Write metadata
        metadata_file = instance_dir / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        return metadata
    
    def _inject_config(self, html: str, config: Dict[str, Any]) -> str:
        """Inject configuration into HTML template"""
        
        # Escape JSON for safe HTML injection
        config_json = json.dumps(config)
        
        # Create configuration script
        config_script = f"""
    <!-- Portal Configuration (Injected) -->
    <script>
    window.PORTAL_CONFIG = {config_json};
    window.PORTAL_INSTANCE_ID = '{config.get("instance", {}).get("id", 'unknown')}';
    window.PORTAL_CONSCIOUSNESS_LEVEL = {config.get("instance", {}).get("consciousness_level", 5)};
    window.PORTAL_GENERATED_AT = '{datetime.now().isoformat()}';
    </script>
    """
        
        # Insert before closing body tag
        if "</body>" in html:
            return html.replace("</body>", f"{config_script}</body>")
        else:
            # Fallback: append to end if no body tag
            return html + config_script
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration schema"""
        
        # Required top-level sections
        required_sections = ["instance", "branding", "api"]
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required section: {section}")
        
        # Instance validation
        instance = config.get("instance", {})
        instance_required = ["name", "id", "account"]
        for field in instance_required:
            if field not in instance:
                raise ValueError(f"Missing instance.{field}")
        
        # Validate consciousness level (1-10)
        consciousness_level = instance.get("consciousness_level", 5)
        if not isinstance(consciousness_level, int) or consciousness_level < 1 or consciousness_level > 10:
            raise ValueError(f"consciousness_level must be integer 1-10, got {consciousness_level}")
        
        # Branding validation
        branding = config.get("branding", {})
        branding_required = ["primary_color", "secondary_color"]
        for field in branding_required:
            if field not in branding:
                raise ValueError(f"Missing branding.{field}")
        
        # Validate hex colors
        for color_field in ["primary_color", "secondary_color", "accent_color"]:
            if color_field in branding:
                color = branding[color_field]
                if not self._is_valid_hex_color(color):
                    raise ValueError(f"Invalid hex color: branding.{color_field} = {color}")
        
        # API validation
        api = config.get("api", {})
        if "base_url" not in api:
            raise ValueError("Missing api.base_url")
        
        # Template type validation
        template_type = config.get("template_type", "consciousness-hub")
        if template_type not in self.VALID_TEMPLATES:
            raise ValueError(f"Invalid template_type: {template_type}. Valid: {list(self.VALID_TEMPLATES.keys())}")
        
        return True
    
    @staticmethod
    def _is_valid_hex_color(color: str) -> bool:
        """Validate hex color format"""
        if not isinstance(color, str):
            return False
        if not color.startswith("#"):
            return False
        hex_part = color[1:]
        if len(hex_part) not in [3, 6]:
            return False
        try:
            int(hex_part, 16)
            return True
        except ValueError:
            return False
    
    def batch_generate(self, configs: list) -> list:
        """Generate multiple portal instances"""
        results = []
        for config in configs:
            try:
                metadata = self.generate(config)
                results.append({
                    "status": "success",
                    "metadata": metadata
                })
            except Exception as e:
                results.append({
                    "status": "error",
                    "instance_id": config.get("instance", {}).get("id", "unknown"),
                    "error": str(e)
                })
        return results
    
    def list_templates(self) -> Dict[str, str]:
        """List available templates"""
        return self.VALID_TEMPLATES.copy()
    
    def get_template_info(self, template_type: str) -> Dict[str, Any]:
        """Get detailed information about a template"""
        if template_type not in self.VALID_TEMPLATES:
            raise ValueError(f"Unknown template: {template_type}")
        
        template_path = self.base_dir / f"{template_type}.html"
        
        return {
            "name": template_type,
            "description": self.VALID_TEMPLATES[template_type],
            "path": str(template_path),
            "exists": template_path.exists(),
            "size_bytes": template_path.stat().st_size if template_path.exists() else 0
        }


def main():
    """CLI interface for portal template generator"""
    
    if len(sys.argv) < 2:
        print("Usage: python portal_template_generator.py <command> [args]")
        print("\nCommands:")
        print("  generate <config.json>     Generate portal from configuration")
        print("  batch <configs.json>       Generate multiple portals")
        print("  list                       List available templates")
        print("  info <template>            Get template information")
        sys.exit(1)
    
    command = sys.argv[1]
    generator = PortalTemplateGenerator()
    
    try:
        if command == "generate":
            if len(sys.argv) < 3:
                print("Error: config.json path required")
                sys.exit(1)
            
            config_path = Path(sys.argv[2])
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            metadata = generator.generate(config)
            print(json.dumps(metadata, indent=2))
        
        elif command == "batch":
            if len(sys.argv) < 3:
                print("Error: configs.json path required")
                sys.exit(1)
            
            configs_path = Path(sys.argv[2])
            with open(configs_path, 'r') as f:
                configs = json.load(f)
            
            results = generator.batch_generate(configs)
            print(json.dumps(results, indent=2))
        
        elif command == "list":
            templates = generator.list_templates()
            print("Available templates:")
            for name, desc in templates.items():
                print(f"  - {name}: {desc}")
        
        elif command == "info":
            if len(sys.argv) < 3:
                print("Error: template name required")
                sys.exit(1)
            
            template_type = sys.argv[2]
            info = generator.get_template_info(template_type)
            print(json.dumps(info, indent=2))
        
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

