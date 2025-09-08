# Dan Holman – Software Developer in Test Portfolio

Welcome to my professional portfolio!  
I’m a **Senior Software Developer in Test (SDET) & Automation Architect** with 13+ years of experience in building automation frameworks, cloud-native solutions, and quality platforms at scale.

This repo highlights examples of my work in **test automation, AWS cloud development, and AI-powered testing**.  
Each folder contains code samples or writeups demonstrating skills I use daily to improve developer velocity, reduce defects, and increase reliability.

---

## 📂 Projects

### 🔹 [Automation Framework](./automation-framework)
A sample Python/TypeScript test automation framework showing:
- Page Object design pattern
- GraphQL & REST API testing
- Contract testing with Pact
- CI/CD integration with GitHub Actions

---

### 🔹 [Cloud-Native App](./cloud-native-app)
An AWS serverless demo app with:
- Lambda + API Gateway + DynamoDB
- Infrastructure as Code (CloudFormation/CDK)
- Integration and contract tests
- GitHub Actions pipeline

---

### 🔹 [AI-Powered Testing](./ai-testing)
Prototype scripts using LLMs to:
- Generate test cases from API schemas
- Reduce manual authoring effort
- Accelerate coverage for unit, integration, and contract tests

---

### 🔹 [Case Studies](./case-studies)
Technical writeups and lessons learned:
- [Contract Testing Strategy](./case-studies/contract-testing.md)  
- [Scaling Test Data with AWS Step Functions](./case-studies/test-data-at-scale.md)  
- [Improving Reliability with CI/CD Quality Gates](./case-studies/ci-cd-quality-gates.md)  

---

## 🔧 Tech Stack

- **Languages:** Python, TypeScript, Java, GraphQL  
- **Cloud & DevOps:** AWS (Lambda, S3, CloudFormation, Step Functions, RDS), GitHub Actions, Jenkins, TeamCity, Datadog  
- **Testing Tools:** Playwright, Pact, Cypress, Selenium, Appium, Postman, Axe  
- **Other:** ReactJS, Docker, SQL, Git

---

## 📫 Connect

- 💼 [LinkedIn](https://linkedin.com/in/danxholman)  
- 📧 [danxholman@gmail.com](mailto:danxholman@gmail.com)

---

## AI Testing: Concepts and How-To

### What are agent rules?
Agent rules constrain and guide model behavior (tone, safety, allowed tools).
- Public rules live in `ai-testing/agents/*.public.yaml`.
- Private rules (full SOPs, tools) live in `ai-private/agents/*.private.yaml`.

### Using code and docs as context
- Put code/docs in the prompt or reference files that your runner loads.
- Example: `evals/cases/summarize.jsonl` points to `evals/example-cf.yaml` as context.
- Your real runner would read the context file and include it in the model input.

### Public vs private content
- Public: sanitized prompts, agent configs, eval harness.
- Private: original prompts/agents/datasets in `ai-private/` (private submodule).
- Generate redacted artifacts: `make redacted` inside `ai-testing/`.

### Running the demo flow
1. `cd ai-testing`
2. `make install`
3. `make eval-run` (simulates a model call and scores output)
4. Inspect `evals/reports/scores.jsonl`

### Env and secrets
- Copy `.env.example` to `.env` and set keys locally.
- Never commit real secrets. Pre-commit hooks help prevent this.


## Working in Cursor
- See `docs/cursor-demo.md` for a guided demo using repo-wide context.
- Keep changes mock-only; no API calls are required.


> Cursor is an AI code editor with repo-wide code awareness, natural language editing, and fast autocomplete. See the official site: https://cursor.com/.

