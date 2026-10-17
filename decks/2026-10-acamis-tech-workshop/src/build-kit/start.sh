#!/bin/bash
# Start Claude Code for the live build with the Toolbox folder attached.
cd "$(dirname "$0")" && exec claude --add-dir ../../../../talks/2026-10-acamis-tech-workshop/build "$@"
