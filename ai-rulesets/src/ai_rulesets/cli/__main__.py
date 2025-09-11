#!/usr/bin/env python3
"""
CLI entry point for ai-rulesets package.
"""

import sys
from .quality_checker import main

if __name__ == "__main__":
    sys.exit(main())
