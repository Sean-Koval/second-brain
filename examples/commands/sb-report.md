Help the user generate a comprehensive work report using the Second Brain CLI.

The CLI command is:
```bash
sb report work [OPTIONS]
```

Options:
- `--days INTEGER` - Number of days to include (default: 7)
- `-p, --project SLUG` - Filter by specific project

Ask the user:
1. What time period? (last 7 days, last 30 days, this month, etc.)
2. Should this be filtered to a specific project?

Calculate the number of days and construct the command:

Examples:
```bash
# Report for last 7 days (default)
sb report work

# Report for last 30 days
sb report work --days 30

# Report for last 2 weeks
sb report work --days 14

# Report for specific project (last week)
sb report work --days 7 --project mobile-app-redesign

# Full quarter report
sb report work --days 90

# Report for specific project (last month)
sb report work --days 30 --project api-v2-migration
```

The report includes:
- Summary statistics (days worked, tasks completed, time spent)
- List of completed tasks with details
- Daily work log entries
- Project breakdown (if not filtered to one project)
- Time tracking totals

Common time periods:
- Last week: `--days 7`
- Last two weeks: `--days 14`
- Last month: `--days 30`
- Last quarter: `--days 90`
- Last 6 months: `--days 180`

After showing the command, offer to:
- Execute it for them if they confirm
- Save the output to a file for documentation:
  ```bash
  sb report work --days 30 > monthly-report.md
  ```
- Generate reports for different time periods
- Explain how they can use this for:
  - Weekly status updates
  - Performance reviews
  - Promotion documentation
  - Time tracking audits

Tip: For performance reviews, run a 90-day report (quarterly):
```bash
sb report work --days 90 > q4-2024-performance.md
```
