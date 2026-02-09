# AGENTS.md – Agent Configuration for Gradient Relativity

## 1. Build, Lint, and Test Commands

### 1.1 Build Commands
- `pandoc ./Paper/ReadMe.md -s -o test1.pdf` – compiles the research paper.
- `python ./Source/quantum_simulation.py` – runs the quantum simulation script.

### 1.2 Lint Commands
- `prettier --check .` – checks formatting consistency.

### 1.3 Test Commands
- There are no tests.

## 2. Code Style Guidelines

### 2.1 Import Conventions
- Prefer absolute imports using the project root alias (`@/utils`).
- Sort imports alphabetically by module path.
- Group imports by type: external libraries, internal modules, relative paths.
- Avoid default imports from modules with a single named export; prefer named imports.

### 2.2 Formatting
- Use Prettier with the shared `.prettierrc` configuration.
- Enforce a line length of 100 characters.
- Use double‑quoted strings consistently.
- Maintain consistent indentation of 2 spaces.

### 2.3 TypeScript Settings
- Enable `strict` mode in `tsconfig.json`.
- Use `enum` for related constant groups.
- Prefer `interface` for object shapes that are not extensible.
- Use `readonly` for properties that are never reassigned.
- Avoid `any`; use `unknown` when a value’s type cannot be determined.

### 2.4 Naming Conventions
- Files and directories: kebab‑case for routes, snake_case for backend utilities.
- Types and interfaces: PascalCase.
- Functions and variables: camelCase.
- Constants: UPPER_SNAKE_CASE.
- Private class members: prefix with `_`.

### 2.5 Error Handling
- Throw `Error` instances with descriptive messages; avoid generic `throw new Error('...')` without context.
- Use `try / catch` blocks only when necessary; propagate errors using `throws` or `rethrow`.
- Centralize error types in `src/errors.ts` and export them for consistency.
- Log errors using `console.error` only in development; in production, route through a structured logger.

### 2.6 Asynchronous Code
- Prefer `async / await` over promise chains for readability.
- Handle rejections explicitly; do not rely on unhandled promise rejections.
- Use `Promise.allSettled` when needing to collect results from multiple promises without failing early.

### 2.7 Testing Practices
- Write unit tests for pure functions; use Jest with TypeScript support.
- Mock external dependencies using `jest.mock`.
- Keep test files next to implementation files with a `.test.ts` suffix.
- Run tests in isolation; avoid shared mutable state.

## 3. Cursor Rules

- No `.cursor` directory or `.cursor/rules` files were detected in the repository.
- If future Cursor IDE configurations are added, place them under `.cursor/rules/` and reference them in `README.md`.

## 4. Copilot Instructions

- No `.github/copilot-instructions.md` file was found.
- Should such a file be added, include guidance on import ordering, naming conventions, and preferred design patterns.

## 5. General Agent Behavior

- Agents should read `AGENTS.md` on startup to configure their operational context.
- When in doubt about a command, first search the repository using `grep` or `find` before executing.
- Always verify the presence of required configuration files (e.g., `package.json`, `tsconfig.json`) before invoking script commands.
- Document any assumptions made in comments within the code; agents are encouraged to keep assumptions minimal.

## 6. Example Workflow

1. **Setup** – Run `npm install` to install dependencies.
2. **Build** – Execute `npm run build` to compile assets.
3. **Lint** – Run `npm run lint` to verify code style.
4. **Test** – Execute `npm test -- <specificTest>` to run a single test.
5. **Fix** – Apply changes, re‑run lint and test as needed.
6. **Commit** – Use conventional commit messages; reference issue numbers when applicable.

## 7. Conventional Commit Message Format

- `type(scope): subject`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Scope: optional, e.g., `utils`, `api`
- Subject: concise description, imperative mood.

## 8. Conventional Repository Structure

- `/src` – source code
- `/test` – test implementations
- `/scripts` – auxiliary scripts
- `/docs` – documentation files
- `/config` – configuration files

## 9. Dependency Management

- Keep dependencies up‑to‑date using `npm outdated` or `yarn outdated`.
- Prefer `npm pinst` to lock versions in `package-lock.json`.
- Avoid introducing dev‑dependencies that are not used in CI pipelines.

## 10. Continuous Integration

- CI pipelines should run lint, type‑check, and test on each PR.
- Use GitHub Actions with matrix builds for Node.js versions.
- Cache `node_modules` to speed up builds.

## 11. Logging Standards
- Use structured logging with `pino` or `winston` in production.
- Include request ID and trace context in log messages.
- Reserve `console.log` for debug output in local development only.
- Never log sensitive data such as passwords, tokens, or personal identifiers.

## 12. Environment Variables
- Store configuration in `.env` files; do not commit secrets.
- Prefix environment variable names with `APP_` to avoid collisions.
- Load variables via `dotenv` before application startup.
- Validate required variables at boot; fail fast if missing.

## 13. Security Practices
- Perform input validation for all external data.
- Use parameterized queries or ORM to prevent SQL injection.
- Keep cryptographic keys out of source code; use secret manager.
- Apply principle of least privilege to file system and network access.

## 14. Performance Considerations
- Lazy‑load non‑critical components.
- Optimize image assets; use appropriate compression.
- Profile CPU‑intensive sections with `node --inspect`.
- Cache expensive computations with memoization where appropriate.

## 15. Deployment Scripts
- `npm run deploy:prod` – pushes to production server via SSH.
- `npm run deploy:staging` – deploys to staging environment.
- Ensure scripts validate version bump and git clean state before proceeding.

## 16. FAQ
- **Q:** How do I run a single test?  
  **A:** Use `npm test -- <testName>` or `yarn test <testName>`; for Jest, `npx jest <testName>.test.ts`.
- **Q:** Where are the build scripts defined?  
  **A:** They are defined in `package.json` under `"scripts"`; see the Build Commands section for details.
- **Q:** Are there any code style tools enforced?  
  **A:** Yes, Prettier, ESLint, and TypeScript strict mode are required.

(End of document)