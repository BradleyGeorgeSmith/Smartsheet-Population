#!/usr/bin/env bash
# Runs at the start of a Claude Code cloud session for this repository.
# Makes sure the one Python library the ToDo Task commands need is present.
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
python3 -c "import docx" 2>/dev/null && exit 0
pip install --quiet "python-docx>=1.1" >/dev/null 2>&1 || echo "ToDo Task: python-docx could not be installed; run pip install python-docx before building Word documents."
exit 0
