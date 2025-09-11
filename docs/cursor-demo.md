# Cursor Demo: Repo-Wide AI Assistance

> Cursor is an AI code editor built to make you extraordinarily productive, with repo-wide code understanding, natural language editing, and powerful autocompletion. Learn more at https://cursor.com/.


This guide shows how to use Cursor to leverage full-repo context beyond typical chat responses.

## Why Cursor here?
- Repo-aware suggestions: understands `automation-framework/`, `cloud-native-app/`, and `ai-test-generation/` at once.
- Tooling integration: read/write files, run commands, and propose structured edits.
- Safer workflows: can be constrained to only modify targeted files and show diffs.

## Suggested demo flow (mock-only)

1) Navigate and index
- Open the repo in Cursor; let it index the project.
- Ask: "Give me a summary of the repo structure and the purpose of each module."

2) Cross-referencing docs and code
- Ask: "Using `ai-test-generation/evals/cases/summarize.jsonl` and `ai-test-generation/evals/example-cf.yaml`, explain how the eval case uses the context file."

3) Add a small feature with edits
- Prompt: "Add a new eval case that checks for the presence of Outputs in a template; name it `outputs.jsonl`."
- Review the proposed edits (Cursor shows diffs), accept or refine.

4) Repo-wide refactor (scoped)
- Prompt: "In `automation-framework/`, add an ESLint config and wire it in the Makefile lint target. Avoid changing other modules."

5) Safety and redaction
- Prompt: "Add a pre-commit message to the README warning not to commit secrets; confirm `.gitignore` excludes `ai-private/` and `.env` files."

## Best practices
- Be explicit about file paths and constraints in prompts.
- Use "show me the diff before applying" to review changes.
- Keep mock-only by not providing real API keys; keep everything in `.env.example`.
- For larger changes, ask Cursor to create TODOs and proceed step-by-step.

## What to highlight live
- Cursor finds related files quickly (e.g., connects Makefile targets with scripts).
- It can read `README.md` + `docs/` + code together to maintain consistency.
- It respects `.gitignore` and won't accidentally include `ai-private/` if configured.

## CI/CD Debugging and Fixing with Cursor

This portfolio demonstrates advanced AI integration in CI/CD pipelines using [Cursor CLI](https://docs.cursor.com/en/cli/github-actions) for automated debugging and fixing of complex CI/CD issues.

### **Problem: Artifact Path Resolution Issues**

The portfolio faced a complex CI/CD issue where:
- **Test artifacts were being uploaded successfully** (142 files uploaded)
- **Deploy workflow was running** but only creating placeholder files
- **GitHub Pages showed "Reports will be available after test execution"** instead of actual test results
- **Root cause**: Nested directory structure in artifacts wasn't being handled correctly

### **Solution: AI-Powered CI/CD Debugging**

#### **1. Enhanced Cursor CLI Integration**

Added comprehensive CI/CD debugging capabilities to the portfolio test suite:

```yaml
- name: Fix CI/CD Issues with Cursor
  if: always() && (github.event.inputs.enable_cursor_fixes != false || github.event_name != 'workflow_dispatch')
  env:
    CURSOR_API_KEY: ${{ secrets.CURSOR_API_KEY }}
  run: |
    echo "🔧 Cursor CLI: Analyzing and fixing CI/CD issues..."
    cursor-agent -p "IMPORTANT: Do NOT create branches, commit, push, or post PR comments. 
    Only modify files in the working directory. 
    Analyze the CI/CD pipeline issues in this run, particularly:
    1. Artifact upload/download problems
    2. Allure report generation failures
    3. Coverage report generation issues
    4. GitHub Pages deployment problems
    5. Path resolution issues in deploy workflows
    
    Check the automation-framework module for:
    - Allure report generation in reports/allure-report/
    - Coverage report generation in reports/coverage/
    - Artifact upload paths and naming
    - Test execution and reporting configuration
    
    Fix any issues that prevent proper artifact generation and deployment to GitHub Pages.
    Focus on ensuring reports are generated correctly and artifacts are uploaded with proper paths."
```

#### **2. Key Features of AI CI/CD Debugging**

**Comprehensive Issue Analysis:**
- **Artifact Upload/Download Problems**: AI analyzes artifact naming, paths, and upload patterns
- **Report Generation Failures**: AI checks Allure, coverage, and other report generation steps
- **Path Resolution Issues**: AI identifies and fixes nested directory structure problems
- **GitHub Pages Deployment**: AI ensures proper file mapping for static site deployment

**Multi-Module Support:**
- **Python Modules**: pytest, Allure, coverage reports
- **TypeScript Modules**: Jest, Playwright, coverage reports
- **Mixed Modules**: Both Python and TypeScript testing in same workflow

**Safe AI Integration:**
- **No Git Operations**: AI only modifies files, never commits or pushes
- **Working Directory Scope**: AI operates within module-specific working directories
- **Restricted Autonomy**: AI can't create branches or post PR comments

#### **3. Debugging Strategy Implementation**

**Step 1: Comprehensive Logging**
```bash
echo "=== DEBUG: artifact structure ==="
find allure-reports/ -type f | head -20
echo "=== DEBUG: Looking for specific paths ==="
ls -la allure-reports/${module}-allure-report/ 2>/dev/null || echo "Path not found"
```

**Step 2: AI Analysis**
- AI analyzes the debug output to identify the exact issue
- AI understands the nested directory structure problem
- AI proposes fixes for path resolution logic

**Step 3: Automated Fixes**
- AI modifies the deploy workflow to handle both possible paths
- AI updates artifact upload/download patterns
- AI ensures proper file copying logic

#### **4. Real-World Benefits**

**Faster Issue Resolution:**
- **Traditional Approach**: Manual debugging, trial and error, multiple iterations
- **AI Approach**: Automated analysis and fixing in single CI run

**Comprehensive Coverage:**
- **Multiple Issue Types**: Test failures, CI/CD problems, deployment issues
- **Cross-Module Understanding**: AI understands relationships between modules
- **Context Awareness**: AI has full repository context for better fixes

**Production-Ready Integration:**
- **Safe Operations**: No risk of accidental commits or pushes
- **Configurable**: Can be enabled/disabled per workflow run
- **Scalable**: Works across all modules and test types

### **Advanced CI/CD Patterns Demonstrated**

#### **1. Artifact Path Resolution**
```bash
# Handle both possible nested directory structures
if [ -d "allure-reports/${module}-allure-report/${module}/reports/allure-report" ]; then
  cp -r allure-reports/${module}-allure-report/${module}/reports/allure-report/* gh-pages-deploy/${module}/
elif [ -d "allure-reports/${module}-allure-report/reports/allure-report" ]; then
  cp -r allure-reports/${module}-allure-report/reports/allure-report/* gh-pages-deploy/${module}/
else
  # Fallback: find any HTML files in the artifact
  find allure-reports/${module}-allure-report -name "*.html" -exec cp {} gh-pages-deploy/${module}/ \;
fi
```

#### **2. Multi-Language CI/CD Support**
- **Python**: pytest, Allure, coverage.py
- **TypeScript**: Jest, Playwright, coverage reports
- **Mixed**: Both languages in same workflow with proper path handling

#### **3. Debugging and Monitoring**
- **Comprehensive Logging**: Detailed debug output for troubleshooting
- **Artifact Validation**: Verify artifacts are uploaded and downloaded correctly
- **Path Verification**: Check that files are copied to correct locations

### **Best Practices for AI CI/CD Integration**

#### **1. Prompt Engineering**
- **Be Specific**: Clearly define what issues to look for
- **Provide Context**: Include module-specific information and constraints
- **Set Boundaries**: Always specify what AI should NOT do (no git operations)

#### **2. Safety Measures**
- **Restricted Scope**: Limit AI to specific directories and file types
- **No Git Operations**: Never allow AI to commit, push, or create branches
- **Review Changes**: Always review AI-proposed changes before applying

#### **3. Debugging Strategy**
- **Comprehensive Logging**: Add detailed debug output to identify issues
- **Step-by-Step Analysis**: Break down complex problems into manageable pieces
- **Fallback Mechanisms**: Provide multiple approaches for path resolution

### **Results and Impact**

**Before AI Integration:**
- Manual debugging of CI/CD issues
- Trial and error approach to fixing path problems
- Multiple iterations to resolve deployment issues

**After AI Integration:**
- Automated analysis and fixing of CI/CD issues
- Single-run resolution of complex path problems
- Proactive identification and fixing of deployment issues

This demonstrates how AI can be effectively integrated into CI/CD pipelines to provide automated debugging, fixing, and optimization capabilities while maintaining safety and reliability.
