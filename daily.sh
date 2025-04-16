#!/bin/bash

echo "▶️ Starting daily banking simulation..."

rm -f transaction_log.txt merged_transaction_log.txt tsession1.txt

python3 main.py

cp transaction_log.txt tsession1.txt
cp tsession1.txt merged_transaction_log.txt

echo "✅ Daily session complete. Merged transaction log saved to merged_transaction_log.txt"
