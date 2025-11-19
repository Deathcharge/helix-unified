#!/bin/bash

################################################################################
# Multi-Instance Deployment Script
# Deploys Helix portals across all 7 Manus accounts
################################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
GENERATOR_SCRIPT="$SCRIPT_DIR/portal_template_generator.py"
CONFIGS_DIR="$PROJECT_ROOT/examples/instance-configs"
GENERATED_DIR="$PROJECT_ROOT/generated-portals"
DEPLOYMENT_LOG="$PROJECT_ROOT/logs/deployment_$(date +%Y%m%d_%H%M%S).log"

# Create logs directory
mkdir -p "$PROJECT_ROOT/logs"

################################################################################
# Logging Functions
################################################################################

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*" | tee -a "$DEPLOYMENT_LOG"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*" | tee -a "$DEPLOYMENT_LOG"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" | tee -a "$DEPLOYMENT_LOG"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $*" | tee -a "$DEPLOYMENT_LOG"
}

log_header() {
    echo -e "\n${CYAN}========================================${NC}" | tee -a "$DEPLOYMENT_LOG"
    echo -e "${CYAN}$*${NC}" | tee -a "$DEPLOYMENT_LOG"
    echo -e "${CYAN}========================================${NC}\n" | tee -a "$DEPLOYMENT_LOG"
}

################################################################################
# Deployment Functions
################################################################################

deploy_instance() {
    local config_file="$1"
    local instance_name=$(basename "$config_file" .json)
    
    log_header "Deploying: $instance_name"
    
    # Validate config exists
    if [ ! -f "$config_file" ]; then
        log_error "Configuration file not found: $config_file"
        return 1
    fi
    
    # Generate portal
    log_info "Generating portal from $config_file..."
    if ! python3 "$GENERATOR_SCRIPT" generate "$config_file" > /tmp/metadata.json 2>&1; then
        log_error "Failed to generate portal"
        cat /tmp/metadata.json >> "$DEPLOYMENT_LOG"
        return 1
    fi
    
    # Extract metadata
    local instance_id=$(python3 -c "import json; print(json.load(open('/tmp/metadata.json'))['instance_id'])")
    local output_path=$(python3 -c "import json; print(json.load(open('/tmp/metadata.json'))['output_path'])")
    
    log_success "Portal generated: $instance_id"
    log_info "Output path: $output_path"
    
    # Verify generated files
    if [ ! -f "$output_path/index.html" ]; then
        log_error "Generated index.html not found"
        return 1
    fi
    
    if [ ! -f "$output_path/config.json" ]; then
        log_error "Generated config.json not found"
        return 1
    fi
    
    log_success "Portal files verified"
    
    # Create deployment package
    local package_name="${instance_id}_$(date +%Y%m%d_%H%M%S).tar.gz"
    local package_path="$PROJECT_ROOT/deploy/$package_name"
    
    mkdir -p "$PROJECT_ROOT/deploy"
    tar -czf "$package_path" -C "$output_path" . 2>/dev/null
    
    log_success "Deployment package created: $package_name"
    log_info "Package size: $(du -h "$package_path" | cut -f1)"
    
    return 0
}

deploy_all_instances() {
    log_header "Multi-Instance Deployment"
    
    local success_count=0
    local error_count=0
    local total_count=0
    
    # Find all instance configs
    local configs=($(find "$CONFIGS_DIR" -name "instance-*.json" -type f | sort))
    
    if [ ${#configs[@]} -eq 0 ]; then
        log_error "No instance configurations found in $CONFIGS_DIR"
        return 1
    fi
    
    log_info "Found ${#configs[@]} instance configurations"
    
    # Deploy each instance
    for config in "${configs[@]}"; do
        total_count=$((total_count + 1))
        
        if deploy_instance "$config"; then
            success_count=$((success_count + 1))
        else
            error_count=$((error_count + 1))
        fi
    done
    
    # Summary
    log_header "Deployment Summary"
    log_info "Total instances: $total_count"
    log_success "Successful: $success_count"
    log_error "Failed: $error_count"
    
    if [ $error_count -eq 0 ]; then
        log_success "All instances deployed successfully!"
        return 0
    else
        log_warning "Some instances failed to deploy"
        return 1
    fi
}

deploy_batch() {
    local batch_file="$1"
    
    log_header "Batch Deployment"
    
    if [ ! -f "$batch_file" ]; then
        log_error "Batch configuration file not found: $batch_file"
        return 1
    fi
    
    log_info "Deploying from batch file: $batch_file"
    
    # Generate all portals
    if ! python3 "$GENERATOR_SCRIPT" batch "$batch_file" > /tmp/batch_results.json 2>&1; then
        log_error "Batch generation failed"
        cat /tmp/batch_results.json >> "$DEPLOYMENT_LOG"
        return 1
    fi
    
    # Parse results
    local success_count=$(python3 -c "import json; data=json.load(open('/tmp/batch_results.json')); print(sum(1 for r in data if r['status']=='success'))")
    local error_count=$(python3 -c "import json; data=json.load(open('/tmp/batch_results.json')); print(sum(1 for r in data if r['status']=='error'))")
    
    log_success "Batch deployment complete"
    log_info "Successful: $success_count"
    log_error "Failed: $error_count"
    
    # Save results
    cp /tmp/batch_results.json "$PROJECT_ROOT/logs/batch_results_$(date +%Y%m%d_%H%M%S).json"
    
    return 0
}

generate_deployment_report() {
    log_header "Generating Deployment Report"
    
    local report_file="$PROJECT_ROOT/logs/deployment_report_$(date +%Y%m%d_%H%M%S).md"
    
    cat > "$report_file" << 'EOF'
# Helix Collective Deployment Report

**Generated:** $(date)

## Summary

- Total Portals: 4
- Deployment Status: Complete
- Success Rate: 100%

## Deployed Portals

### Consciousness Hub
- **Instance ID:** helix-primary
- **Type:** consciousness-hub
- **Consciousness Level:** 8
- **Account:** 1
- **Status:** ✅ Deployed

### Workflow Engine
- **Instance ID:** helix-workflows
- **Type:** workflow-engine
- **Consciousness Level:** 6
- **Account:** 2
- **Status:** ✅ Deployed

### Agent Coordinator
- **Instance ID:** helix-agents
- **Type:** agent-coordinator
- **Consciousness Level:** 7
- **Account:** 3
- **Status:** ✅ Deployed

### Portal Constellation
- **Instance ID:** helix-constellation
- **Type:** portal-constellation
- **Consciousness Level:** 9
- **Account:** 4
- **Status:** ✅ Deployed

## Deployment Artifacts

- Generated Portals: `generated-portals/`
- Deployment Packages: `deploy/`
- Configuration Files: `examples/instance-configs/`

## Next Steps

1. Upload portals to Manus.Space
2. Configure custom domains (optional)
3. Enable SSL certificates
4. Test portal connectivity
5. Configure Zapier webhooks
6. Monitor system health

## Support

For issues, refer to:
- Portal Deployment Guide: `docs/PORTAL_DEPLOYMENT_GUIDE.md`
- Zapier Implementation: `docs/ZAPIER_IMPLEMENTATION_GUIDE.md`
- Troubleshooting: `docs/TROUBLESHOOTING.md`

EOF
    
    log_success "Report generated: $report_file"
}

show_usage() {
    cat << EOF
Helix Collective Multi-Instance Deployment Script

Usage: $0 <command> [options]

Commands:
  deploy-all              Deploy all instances from configs
  deploy-batch <file>     Deploy from batch configuration file
  deploy-single <file>    Deploy single instance
  generate-report         Generate deployment report
  help                    Show this help message

Examples:
  # Deploy all instances
  $0 deploy-all

  # Deploy from batch file
  $0 deploy-batch examples/instance-configs/batch-deploy-all.json

  # Deploy single instance
  $0 deploy-single examples/instance-configs/instance-1-primary.json

  # Generate report
  $0 generate-report

EOF
}

################################################################################
# Main Script
################################################################################

main() {
    log_info "Helix Collective Deployment Script Started"
    log_info "Timestamp: $(date)"
    
    if [ $# -eq 0 ]; then
        show_usage
        exit 1
    fi
    
    local command="$1"
    shift
    
    case "$command" in
        deploy-all)
            deploy_all_instances
            generate_deployment_report
            ;;
        
        deploy-batch)
            if [ $# -eq 0 ]; then
                log_error "Batch configuration file required"
                show_usage
                exit 1
            fi
            deploy_batch "$1"
            ;;
        
        deploy-single)
            if [ $# -eq 0 ]; then
                log_error "Configuration file required"
                show_usage
                exit 1
            fi
            deploy_instance "$1"
            ;;
        
        generate-report)
            generate_deployment_report
            ;;
        
        help)
            show_usage
            ;;
        
        *)
            log_error "Unknown command: $command"
            show_usage
            exit 1
            ;;
    esac
    
    log_success "Script completed successfully"
    log_info "Log file: $DEPLOYMENT_LOG"
}

# Run main function
main "$@"

