# Tinybird Workspace Management Scripts

This directory contains scripts and workflows for managing Tinybird workspaces, including workspace creation and data migration between workspaces.

## Files

- `migrate_tinybird_data.sh` - Standalone script for migrating data between workspaces
- `../.github/workflows/tinybird-workspace-creation.yml` - GitHub workflow for creating new workspaces

## GitHub Workflow: Workspace Creation

The `tinybird-workspace-creation.yml` workflow allows you to create new Tinybird workspaces with all resources from the `tinybird/` folder and optionally copy the last partition data from an existing workspace.

### Usage

1. Go to your GitHub repository
2. Navigate to **Actions** tab
3. Select **Tinybird Workspace Creation and Data Migration**
4. Click **Run workflow**
5. Fill in the required parameters:
   - **Source workspace**: Name of the existing workspace to copy data from
   - **Target workspace**: Name of the new workspace to create
   - **Copy data**: Whether to copy the last partition data (default: true)
   - **Source token**: Token for source workspace (optional, uses default if not provided)
   - **Target token**: Token for target workspace (optional, will be auto-detected from the workspace)

### What the workflow does

1. **Validates inputs** - Ensures source and target workspaces are different
2. **Creates new workspace** - Creates a new Tinybird workspace with the specified name
3. **Deploys resources** - Deploys all datasources, endpoints, and materializations from the `tinybird/` folder
4. **Verifies deployment** - Lists all deployed resources to confirm successful deployment
5. **Copies data** (optional) - Migrates the last partition from each datasource in the source workspace
6. **Runs tests** - Executes all tests against the new workspace
7. **Generates summary** - Creates a detailed summary of the workspace creation process
8. **Cleanup on failure** - Removes the workspace if any step fails

### Required Secrets

Make sure these secrets are configured in your GitHub repository:

- `TINYBIRD_HOST` - Your Tinybird host URL (e.g., `https://api.tinybird.co`)
- `TINYBIRD_TOKEN` - Your default Tinybird API token

## Standalone Script: Data Migration

The `migrate_tinybird_data.sh` script provides a command-line interface for migrating data between Tinybird workspaces.

### Installation

1. Make sure the script is executable:
   ```bash
   chmod +x scripts/migrate_tinybird_data.sh
   ```

2. Install Tinybird CLI if not already installed:
   ```bash
   curl https://tinybird.co | sh
   ```

### Usage

#### Basic Usage

```bash
# Migrate all datasources from staging to production
./scripts/migrate_tinybird_data.sh \
  -s staging \
  -t production \
  -h https://api.tinybird.co
```

#### Advanced Usage

```bash
# Migrate specific datasource only
./scripts/migrate_tinybird_data.sh \
  -s staging \
  -t production \
  -h https://api.tinybird.co \
  -d landing_ds

# Use different tokens for source and target
./scripts/migrate_tinybird_data.sh \
  -s staging \
  -t production \
  -h https://api.tinybird.co \
  --source-token "your_source_token" \
  --target-token "your_target_token"

# Dry run to see what would be migrated
./scripts/migrate_tinybird_data.sh \
  -s staging \
  -t production \
  -h https://api.tinybird.co \
  --dry-run
```

### Command Line Options

| Option | Description | Required |
|--------|-------------|----------|
| `-s, --source-workspace` | Source workspace name | Yes |
| `-t, --target-workspace` | Target workspace name | Yes |
| `-h, --host` | Tinybird host URL | Yes |
| `--source-token` | Source workspace token | No (uses `TINYBIRD_TOKEN` env var) |
| `--target-token` | Target workspace token | No (auto-detected from workspace) |
| `-d, --datasource` | Specific datasource to migrate | No (migrates all) |
| `--dry-run` | Show what would be done without executing | No |
| `-v, --verbose` | Verbose output | No |
| `--help` | Show help message | No |

### Environment Variables

- `TINYBIRD_TOKEN` - Default Tinybird API token (used if `--source-token` not provided, and for auto-detecting target token)

### Examples

#### Example 1: Migrate from Development to Staging

```bash
export TINYBIRD_TOKEN="your_token_here"
./scripts/migrate_tinybird_data.sh \
  -s development \
  -t staging \
  -h https://api.tinybird.co
```

#### Example 2: Migrate Specific Datasource with Dry Run

```bash
./scripts/migrate_tinybird_data.sh \
  -s staging \
  -t production \
  -h https://api.tinybird.co \
  -d tracker_logs \
  --dry-run
```

#### Example 3: Migrate with Different Tokens

```bash
./scripts/migrate_tinybird_data.sh \
  -s staging \
  -t production \
  -h https://api.tinybird.co \
  --source-token "staging_token" \
  --target-token "production_token"
```

## Auto-Detection of Target Token

Both the workflow and script automatically detect the target workspace token when it's not provided:

1. **Workflow**: After creating the new workspace, the workflow extracts the token from the workspace information
2. **Script**: Uses the `tb workspace ls` command to get workspace information and extract the token

This eliminates the need to manually provide the target token, which is generated when the workspace is created.

## Data Migration Process

Both the workflow and script follow the same data migration process:

1. **Identify datasources** - Get list of datasources to migrate
2. **Get last partition** - For each datasource, find the most recent partition
3. **Export data** - Export the partition data from source workspace
4. **Import data** - Import the data to target workspace
5. **Cleanup** - Remove temporary files

## Error Handling

- **Workspace validation** - Ensures source and target workspaces exist and are accessible
- **Partition validation** - Handles cases where datasources have no partitions
- **Data validation** - Verifies exported data before importing
- **Cleanup on failure** - Removes temporary files even if migration fails

## Best Practices

1. **Always use dry-run first** - Test your migration parameters before executing
2. **Backup important data** - Ensure you have backups before migrating production data
3. **Use specific datasources** - When possible, migrate only the datasources you need
4. **Monitor the process** - Check the output for any warnings or errors
5. **Verify results** - After migration, verify that data was copied correctly

## Troubleshooting

### Common Issues

1. **"Tinybird CLI is not installed"**
   - Install the CLI: `curl https://tinybird.co | sh`

2. **"Workspace not found"**
   - Verify workspace names are correct
   - Check that your token has access to the workspaces

3. **"No partitions found"**
   - This is normal for new or empty datasources
   - The script will skip these datasources

4. **"Permission denied"**
   - Ensure the script is executable: `chmod +x scripts/migrate_tinybird_data.sh`

### Getting Help

- Use `--help` flag to see all available options
- Use `--dry-run` to test your configuration
- Check the script output for detailed error messages 