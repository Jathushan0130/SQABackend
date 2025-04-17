#!/usr/bin/env bash
set -euo pipefail

for day in {1..7}; do
  echo
  echo "########## Day $day ##########"
  ./daily.sh

  # Archive this day’s end‑of‑day accounts and merged transactions
  cp currentaccounts.txt               currentaccounts_day${day}.txt
  cp merged_daily_transactions.txt merged_transactions_day${day}.txt

  echo "Archived Day $day →"
  echo "  currentaccounts_day${day}.txt"
  echo "  merged_transactions_day${day}.txt"
done

echo
echo "=== Weekly run (7 days) complete ==="
