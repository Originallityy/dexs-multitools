#!/bin/bash

# Fix line endings for Ruby scripts
find /workspaces/dexs-multitools -name "*.rb" -type f -exec sed -i 's/\r$//' {} \;

echo "Line endings fixed for Ruby scripts"
