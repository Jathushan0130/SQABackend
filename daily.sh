#!/usr/bin/env bash
set -euo pipefail

# Clean up any old artifacts
rm -f transactions_day_session*.txt merged_daily_transactions.txt

# Replay each of the 9 transaction sessions
for i in {1..9}; do
  session="session${i}.txt"
  out="transactions_day_session${i}.txt"
  echo "→ Running session $i from $session"
  python3 frontend.py < "$session"
  mv transaction_log.txt "$out"
done

# Merge all 9 into one file
echo "→ Merging into merged_daily_transactions.txt"
cat transactions_day_session*.txt > merged_daily_transactions.txt

echo "=== Daily run complete ==="
