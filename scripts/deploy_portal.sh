#!/bin/bash

################################################################################
# Portal Deployment Automation Script
# Deploys customized portal instances to Manus.Space with configuration
################################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
GENERATOR_SCRIPT="$SCRIPT_DIR/portal_template_generator.py"
GENERATED_PORTALS_DIR="$PROJECT_ROOT/generated-portals"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$PROJECT_ROOT/logs/deployment_${TIMESTAMP}.log"

# Create logs directory
mkdir -p "$PROJECT_ROOT/logs"

################################################################################
# Logging Functions
################################################################################

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $*" | tee -a "$LOG_FILE"
}

################################################################################
# Validation Functions
################################################################################

check_requirements() {
    log_info "Checking requirements..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is required but not installed"
        exit 1
    fi
    
    # Check generator script
    if [ ! -f "$GENERATOR_SCRIPT" ]; then
        log_error "Generator script not found: $GENERATOR_SCRIPT"
        exit 1
    fi
    
    log_success "All requirements met"
}

validate_config_file() {
    local config_file="$1"
    
    if [ ! -f "$config_file" ]; then
        log_error "Configuration file not found: $config_file"
        return 1
    fi
    
    # Validate JSON
    if ! python3 -m json.tool "$config_file" > /dev/null 2>&1; then
        log_error "Invalid JSON in configuration file: $config_file"
        return 1
    fi
    
    log_success "Configuration file validated: $config_file"
    return 0
}

################################################################################
# Portal Generation Functions
################################################################################

generate_portal() {
    local config_file="$1"
    
    log_info "Generating portal from configuration: $config_file"
    
    # Run generator
    if python3 "$GENERATOR_SCRIPT" generate "$config_file" > /tmp/portal_metadata.json 2>&1; then
        local metadata=$(cat /tmp/portal_metadata.json)
        local instance_id=$(echo "$metadata" | python3 -c "import sys, json; print(json.load(sys.stdin)['instance_id'])")
        local output_path=$(echo "$metadata" | python3 -c "import sys, json; print(json.load(sys.stdin)['output_path'])")
        
        log_success "Portal generated successfully"
        log_info "Instance ID: $instance_id"
        log_info "Output path: $output_path"
        
        echo "$output_path"
        return 0
    else
        log_error "Failed to generate portal"
        cat /tmp/portal_metadata.json >> "$LOG_FILE"
        return 1
    fi
}

################################################################################
# Deployment Functions
################################################################################

deploy_to_manus_space() {
    local portal_dir="$1"
    local instance_id="$2"
    
    log_info "Deploying portal to Manus.Space: $instance_id"
    
    # Check if portal directory exists
    if [ ! -d "$portal_dir" ]; then
        log_error "Portal directory not found: $portal_dir"
        return 1
    fi
    
    # Check for index.html
    if [ ! -f "$portal_dir/index.html" ]; then
        log_error "Portal index.html not found: $portal_dir/index.html"
        return 1
    fi
    
    # Create deployment package
    local deploy_package="$PROJECT_ROOT/deploy_${instance_id}_${TIMESTAMP}.tar.gz"
    tar -czf "$deploy_package" -C "$portal_dir" .
    
    log_success "Deployment package created: $deploy_package"
    log_info "Package size: $(du -h "$deploy_package" | cut -f1)"
    
    # Note: Actual deployment to Manus.Space would use their API
    # This is a placeholder for the deployment logic
    log_warning "Deployment to Manus.Space requires manual upload or API integration"
    log_info "Package ready for deployment: $deploy_package"
    
    return 0
}

################################################################################
# Batch Deployment Functions
################################################################################

batch_generate_portals() {
    local configs_file="$1"
    
    if [ ! -f "$configs_file" ]; then
        log_error "Batch configurations file not found: $configs_file"
        return 1
    fi
    
    log_info "Starting batch portal generation from: $configs_file"
    
    # Run batch generator
    if python3 "$GENERATOR_SCRIPT" batch "$configs_file" > /tmp/batch_results.json 2>&1; then
        local results=$(cat /tmp/batch_results.json)
        
        # Parse results
        local success_count=$(echo "$results" | python3 -c "import sys, json; data=json.load(sys.stdin); print(sum(1 for r in data if r['status']=='success'))")
        local error_count=$(echo "$results" | python3 -c "import sys, json; data=json.load(sys.stdin); print(sum(1 for r in data if r['status']=='error'))")
        
        log_success "Batch generation complete"
        log_info "Successful: $success_count"
        log_warning "Failed: $error_count"
        
        # Save results
        cp /tmp/batch_results.json "$PROJECT_ROOT/logs/batch_results_${TIMESTAMP}.json"
        
        return 0
    else
        log_error "Batch generation failed"
        cat /tmp/batch_results.json >> "$LOG_FILE"
        return 1
    fi
}

################################################################################
# Testing Functions
################################################################################

test_portal() {
    local portal_dir="$1"
    
    log_info "Testing portal: $portal_dir"
    
    # Check required files
    local required_files=("index.html" "config.json" "metadata.json")
    for file in "${required_files[@]}"; do
        if [ ! -f "$portal_dir/$file" ]; then
            log_error "Missing required file: $file"
            return 1
        fi
    done
    
    # Validate HTML
    if ! grep -q "PORTAL_CONFIG" "$portal_dir/index.html"; then
        log_error "Portal configuration not injected in HTML"
        return 1
    fi
    
    # Validate JSON files
    for file in config.json metadata.json; do
        if ! python3 -m json.tool "$portal_dir/$file" > /dev/null 2>&1; then
            log_error "Invalid JSON in $file"
            return 1
        fi
    done
    
    log_success "Portal tests passed"
    return 0
}

################################################################################
# Reporting Functions
################################################################################

generate_deployment_report() {
    local portal_dir="$1"
    local report_file="$PROJECT_ROOT/logs/deployment_report_${TIMESTAMP}.md"
    
    log_info "Generating deployment report: $report_file"
    
    cat > "$report_file" << EOF
# Portal Deployment Report

**Generated:** $(date)  
**Timestamp:** $TIMESTAMP

## Portal Information

EOF
    
    if [ -f "$portal_dir/metadata.json" ]; then
        python3 << PYTHON_EOF >> "$report_file"
import json
with open("$portal_dir/metadata.json") as f:
    metadata = json.load(f)
    print(f"**Instance ID:** {metadata.get('instance_id', 'N/A')}")
    print(f"**Instance Name:** {metadata.get('instance_name', 'N/A')}")
    print(f"**Template Type:** {metadata.get('template_type', 'N/A')}")
    print(f"**Consciousness Level:** {metadata.get('consciousness_level', 'N/A')}")
    print(f"**Account:** {metadata.get('account', 'N/A')}")
    print()
    print("## Files Generated")
    print()
    for name, path in metadata.get('files', {}).items():
        print(f"- **{name}:** {path}")
PYTHON_EOF
    fi
    
    cat >> "$report_file" << EOF

## Deployment Status

- Status: Ready for deployment
- Package Location: $GENERATED_PORTALS_DIR
- Log File: $LOG_FILE

## Next Steps

1. Review configuration in $portal_dir/config.json
2. Test portal locally if possible
3. Upload to Manus.Space using management dashboard
4. Verify portal accessibility
5. Test API integrations and webhooks

EOF
    
    log_success "Report generated: $report_file"
}

################################################################################
# Main Functions
################################################################################

show_usage() {
    cat << EOF
Portal Deployment Automation Script

Usage: $0 <command> [options]

Commands:
  generate <config.json>          Generate portal from configuration file
  batch <configs.json>            Generate multiple portals from batch file
  test <portal_dir>               Test generated portal
  list-templates                  List available templates
  help                            Show this help message

Examples:
  # Generate single portal
  $0 generate configs/instance-1.json

  # Generate multiple portals
  $0 batch configs/all-instances.json

  # Test generated portal
  $0 test generated-portals/instance-1

  # List available templates
  $0 list-templates

EOF
}

################################################################################
# Main Script
################################################################################

main() {
    log_info "Portal Deployment Script Started"
    log_info "Timestamp: $TIMESTAMP"
    
    # Check requirements
    check_requirements
    
    # Parse command
    if [ $# -eq 0 ]; then
        show_usage
        exit 1
    fi
    
    local command="$1"
    shift
    
    case "$command" in
        generate)
            if [ $# -eq 0 ]; then
                log_error "Configuration file required"
                show_usage
                exit 1
            fi
            
            local config_file="$1"
            validate_config_file "$config_file"
            
            local portal_dir=$(generate_portal "$config_file")
            test_portal "$portal_dir"
            generate_deployment_report "$portal_dir"
            
            log_success "Portal generation and testing complete"
            ;;
        
        batch)
            if [ $# -eq 0 ]; then
                log_error "Batch configurations file required"
                show_usage
                exit 1
            fi
            
            local configs_file="$1"
            batch_generate_portals "$configs_file"
            
            log_success "Batch portal generation complete"
            ;;
        
        test)
            if [ $# -eq 0 ]; then
                log_error "Portal directory required"
                show_usage
                exit 1
            fi
            
            local portal_dir="$1"
            test_portal "$portal_dir"
            
            log_success "Portal testing complete"
            ;;
        
        list-templates)
            log_info "Available templates:"
            python3 "$GENERATOR_SCRIPT" list
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
    log_info "Log file: $LOG_FILE"
}

# Run main function
main "$@"

