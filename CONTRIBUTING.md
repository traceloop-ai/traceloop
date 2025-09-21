# Contributing to Traceloop

Thank you for your interest in contributing to Traceloop! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Go 1.21+
- Python 3.8+
- Node.js 18+ (for web dashboard)
- Make
- Git

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/traceloop.git
   cd traceloop
   ```

2. **Initialize the development environment**
   ```bash
   make init
   ```

3. **Run tests to ensure everything works**
   ```bash
   make test
   ```

## 🏗️ Development Workflow

### Branch Strategy

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - Feature branches
- `bugfix/*` - Bug fix branches
- `hotfix/*` - Critical fixes

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code following our style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Run the test suite**
   ```bash
   make test
   make lint
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 Code Style Guidelines

### Go Code

- Follow the standard Go formatting: `go fmt`
- Use meaningful variable and function names
- Add comments for exported functions
- Keep functions small and focused
- Use `golangci-lint` for additional checks

### Python Code

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Format with `black` and `isort`
- Use `mypy` for type checking
- Keep functions under 50 lines when possible

### Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(sdk): add automatic instrumentation for LangChain
fix(server): resolve memory leak in trace storage
docs: update installation guide for Docker
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Run Go tests only
make test-go

# Run Python tests only
make test-python

# Run tests with coverage
make test-coverage
```

### Writing Tests

- Write unit tests for all new functionality
- Aim for >80% code coverage
- Use descriptive test names
- Test both success and error cases
- Mock external dependencies

### Test Structure

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── e2e/           # End-to-end tests
└── fixtures/      # Test data and fixtures
```

## 📚 Documentation

### Code Documentation

- Document all exported functions and types
- Use clear, concise language
- Include examples for complex functions
- Update documentation when changing APIs

### User Documentation

- Update README.md for user-facing changes
- Add examples to the examples/ directory
- Update API documentation for SDK changes

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected behavior** vs actual behavior
4. **Environment details** (OS, Go version, Python version)
5. **Logs and error messages** (if applicable)

## 💡 Feature Requests

When suggesting features:

1. **Check existing issues** to avoid duplicates
2. **Describe the use case** and problem it solves
3. **Provide examples** of how it would work
4. **Consider implementation complexity**

## 🔍 Code Review Process

### For Contributors

1. **Self-review** your code before submitting
2. **Address feedback** promptly and constructively
3. **Keep PRs focused** - one feature per PR
4. **Update tests and docs** as needed

### For Reviewers

1. **Be constructive** and respectful
2. **Focus on code quality** and maintainability
3. **Test the changes** locally when possible
4. **Approve promptly** for good changes

## 🚀 Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- `MAJOR`: Breaking changes
- `MINOR`: New features (backward compatible)
- `PATCH`: Bug fixes (backward compatible)

### Release Steps

1. **Update version numbers** in all relevant files
2. **Update CHANGELOG.md** with new features and fixes
3. **Create a release PR** with version bump
4. **Tag the release** after merge
5. **Publish packages** to PyPI, Docker Hub, etc.

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different opinions and approaches

### Getting Help

- 💬 [Discord Community](https://discord.gg/traceloop)
- 🐛 [GitHub Issues](https://github.com/traceloop-ai/traceloop/issues)
- 📧 [Email](mailto:dev@traceloop-ai.dev)

## 🏆 Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- GitHub contributor graphs
- Community highlights

## 📋 Checklist for PRs

Before submitting a Pull Request, ensure:

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Commit messages follow conventional format
- [ ] PR description is clear and complete
- [ ] Breaking changes are documented

Thank you for contributing to Traceloop! 🎉
