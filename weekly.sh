#!/bin/bash

echo "📅 Starting full weekly banking simulation..."
rm -f day*_current.txt day*_merged_log.txt

for day in {1..7}
do
    echo ""
    echo "============================="
    echo "📆 DAY $day"
    echo "============================="

    ./daily.sh

    cp currentaccounts.txt day${day}_current.txt
    cp merged_transaction_log.txt day${day}_merged_log.txt

    echo "📦 Day $day saved: day${day}_current.txt and day${day}_merged_log.txt"
done

echo ""
echo "✅ Weekly simulation complete. All 7 days logged."
