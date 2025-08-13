#!/bin/bash

# Tinybird Data Migration Script
# This script migrates the last partition data from one workspace to another

set -e

# Default values
SOURCE_WORKSPACE=""
TARGET_WORKSPACE=""
SOURCE_TOKEN=""
TARGET_TOKEN=""
TINYBIRD_HOST=""
DATASOURCE_NAME=""
DRY_RUN=false
VERBOSE=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to show usage
show_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Tinybird Data Migration Script

OPTIONS:
    -s, --source-workspace NAME    Source workspace name (required)
    -t, --target-workspace NAME    Target workspace name (required)
    -h, --host HOST                Tinybird host URL (required)
    --source-token TOKEN           Source workspace token (optional)
    --target-token TOKEN           Target workspace token (optional, will be auto-detected if not provided)
    -d, --datasource NAME          Specific datasource to migrate (optional)
    --dry-run                      Show what would be done without executing
    -v, --verbose                  Verbose output
    --help                         Show this help message

EXAMPLES:
    # Migrate all datasources from staging to production
    $0 -s staging -t production -h https://api.tinybird.co

    # Migrate specific datasource
    $0 -s staging -t production -h https://api.tinybird.co -d landing_ds

    # Dry run to see what would be migrated
    $0 -s staging -t production -h https://api.tinybird.co --dry-run

    # Use specific tokens for both workspaces
    $0 -s staging -t production -h https://api.tinybird.co --source-token "src_token" --target-token "tgt_token"

EOF
}

# Function to validate required parameters
validate_params() {
    if [ -z "$SOURCE_WORKSPACE" ]; then
        print_error "Source workspace is required"
        exit 1
    fi
    
    if [ -z "$TARGET_WORKSPACE" ]; then
        print_error "Target workspace is required"
        exit 1
    fi
    
    if [ -z "$TINYBIRD_HOST" ]; then
        print_error "Tinybird host is required"
        exit 1
    fi
    
    if [ "$SOURCE_WORKSPACE" = "$TARGET_WORKSPACE" ]; then
        print_error "Source and target workspaces cannot be the same"
        exit 1
    fi
}

# Function to check if Tinybird CLI is installed
check_tinybird_cli() {
    if ! command -v tb &> /dev/null; then
        print_error "Tinybird CLI is not installed. Please install it first:"
        echo "curl https://tinybird.co | sh"
        exit 1
    fi
}

# Function to get datasource list
get_datasource_list() {
    local workspace=$1
    local token=$2
    
    if [ -n "$DATASOURCE_NAME" ]; then
        echo "$DATASOURCE_NAME"
    else
        # Get all datasources from the workspace
        tb datasource ls \
            --host "$TINYBIRD_HOST" \
            --token "$token" \
            --workspace "$workspace" \
            --format json | jq -r '.[].name' 2>/dev/null || echo ""
    fi
}

# Function to migrate single datasource
migrate_datasource() {
    local datasource_name=$1
    local source_token=$2
    local target_token=$3
    
    print_info "Processing datasource: $datasource_name"
    
    # Get the last partition from source workspace
    print_info "Getting last partition from source workspace..."
    local last_partition=$(tb datasource partition ls "$datasource_name" \
        --host "$TINYBIRD_HOST" \
        --token "$source_token" \
        --workspace "$SOURCE_WORKSPACE" \
        --format json | jq -r '.[-1].name' 2>/dev/null || echo "")
    
    if [ -z "$last_partition" ] || [ "$last_partition" = "null" ]; then
        print_warning "No partitions found for datasource: $datasource_name"
        return 0
    fi
    
    print_info "Found last partition: $last_partition"
    
    if [ "$DRY_RUN" = true ]; then
        print_info "[DRY RUN] Would copy partition $last_partition for $datasource_name"
        return 0
    fi
    
    # Create a temporary directory for the data
    local temp_dir=$(mktemp -d)
    
    # Export data from source workspace
    print_info "Exporting data from source workspace..."
    tb datasource partition export "$datasource_name" "$last_partition" \
        --host "$TINYBIRD_HOST" \
        --token "$source_token" \
        --workspace "$SOURCE_WORKSPACE" \
        --output "$temp_dir/${datasource_name}_${last_partition}.parquet"
    
    # Import data to target workspace
    if [ -f "$temp_dir/${datasource_name}_${last_partition}.parquet" ]; then
        print_info "Importing data to target workspace..."
        tb datasource append "$datasource_name" \
            --host "$TINYBIRD_HOST" \
            --token "$target_token" \
            --workspace "$TARGET_WORKSPACE" \
            "$temp_dir/${datasource_name}_${last_partition}.parquet"
        
        print_success "Successfully copied partition $last_partition for $datasource_name"
    else
        print_warning "No data file found for $datasource_name partition $last_partition"
    fi
    
    # Clean up temporary directory
    rm -rf "$temp_dir"
}

# Function to get workspace token
get_workspace_token() {
    local workspace=$1
    local default_token=$2
    
    print_info "Getting token for workspace: $workspace"
    
    # Get workspace information with retry logic
    local workspace_info=""
    local retry_count=0
    local max_retries=3
    
    while [ $retry_count -lt $max_retries ]; do
        workspace_info=$(tb workspace ls \
            --host "$TINYBIRD_HOST" \
            --token "$default_token" \
            --format json | jq -r ".[] | select(.name == \"$workspace\")" 2>/dev/null || echo "")
        
        if [ -n "$workspace_info" ] && [ "$workspace_info" != "null" ]; then
            break
        fi
        
        retry_count=$((retry_count + 1))
        if [ $retry_count -lt $max_retries ]; then
            print_warning "Workspace not found, retrying in 5 seconds... (attempt $retry_count/$max_retries)"
            sleep 5
        fi
    done
    
    if [ -z "$workspace_info" ] || [ "$workspace_info" = "null" ]; then
        print_error "Workspace '$workspace' not found or not accessible after $max_retries attempts"
        return 1
    fi
    
    # Extract the token
    local token=$(echo "$workspace_info" | jq -r '.token')
    
    if [ -z "$token" ] || [ "$token" = "null" ]; then
        print_error "Failed to extract token for workspace '$workspace'"
        if [ "$VERBOSE" = true ]; then
            echo "Workspace info: $workspace_info"
        fi
        return 1
    fi
    
    echo "$token"
}

# Function to check workspace connectivity
check_workspace_connectivity() {
    local workspace=$1
    local token=$2
    local workspace_type=$3
    
    print_info "Checking connectivity to $workspace_type workspace: $workspace"
    
    if ! tb workspace ls \
        --host "$TINYBIRD_HOST" \
        --token "$token" | grep -q "$workspace"; then
        print_error "$workspace_type workspace '$workspace' not found or not accessible"
        exit 1
    fi
    
    print_success "$workspace_type workspace connectivity verified"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -s|--source-workspace)
            SOURCE_WORKSPACE="$2"
            shift 2
            ;;
        -t|--target-workspace)
            TARGET_WORKSPACE="$2"
            shift 2
            ;;
        -h|--host)
            TINYBIRD_HOST="$2"
            shift 2
            ;;
        --source-token)
            SOURCE_TOKEN="$2"
            shift 2
            ;;
        --target-token)
            TARGET_TOKEN="$2"
            shift 2
            ;;
        -d|--datasource)
            DATASOURCE_NAME="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Main execution
main() {
    print_info "Starting Tinybird data migration..."
    
    # Validate parameters
    validate_params
    
    # Check if Tinybird CLI is installed
    check_tinybird_cli
    
    # Set source token if not provided
    if [ -z "$SOURCE_TOKEN" ]; then
        SOURCE_TOKEN="${TINYBIRD_TOKEN:-}"
        if [ -z "$SOURCE_TOKEN" ]; then
            print_error "Source token is required. Set TINYBIRD_TOKEN environment variable or use --source-token"
            exit 1
        fi
    fi
    
    # Set target token if not provided (auto-detect from workspace)
    if [ -z "$TARGET_TOKEN" ]; then
        print_info "Target token not provided, auto-detecting from workspace..."
        TARGET_TOKEN=$(get_workspace_token "$TARGET_WORKSPACE" "$SOURCE_TOKEN")
        if [ $? -ne 0 ]; then
            print_error "Failed to auto-detect target token. Please provide --target-token"
            exit 1
        fi
        print_success "Target token auto-detected: ${TARGET_TOKEN:0:10}..."
    fi
    
    # Check workspace connectivity
    check_workspace_connectivity "$SOURCE_WORKSPACE" "$SOURCE_TOKEN" "Source"
    check_workspace_connectivity "$TARGET_WORKSPACE" "$TARGET_TOKEN" "Target"
    
    # Get list of datasources to migrate
    print_info "Getting list of datasources to migrate..."
    local datasources=$(get_datasource_list "$SOURCE_WORKSPACE" "$SOURCE_TOKEN")
    
    if [ -z "$datasources" ]; then
        print_warning "No datasources found in source workspace"
        exit 0
    fi
    
    print_info "Found datasources: $(echo "$datasources" | tr '\n' ' ')"
    
    # Migrate each datasource
    local success_count=0
    local total_count=0
    
    while IFS= read -r datasource; do
        if [ -n "$datasource" ]; then
            total_count=$((total_count + 1))
            if migrate_datasource "$datasource" "$SOURCE_TOKEN" "$TARGET_TOKEN"; then
                success_count=$((success_count + 1))
            fi
        fi
    done <<< "$datasources"
    
    # Summary
    print_success "Migration completed!"
    print_info "Successfully migrated: $success_count/$total_count datasources"
    
    if [ "$DRY_RUN" = true ]; then
        print_warning "This was a dry run. No actual data was migrated."
    fi
}

# Run main function
main "$@" 