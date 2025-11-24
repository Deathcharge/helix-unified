# Contributing to Helix Unified

Thank you for your interest in contributing to Helix Unified! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository**
   ```bash
   gh repo fork Deathcharge/helix-unified
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/helix-unified.git
   cd helix-unified
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use type hints where possible
- Write descriptive variable and function names
- Keep functions focused and concise
- Add docstrings to all functions and classes

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for 80%+ code coverage
- Run tests with: `pytest`

### Documentation

- Update documentation for new features
- Add docstrings to new functions/classes
- Update README.md if needed
- Include examples where helpful

### Commit Messages

Use clear, descriptive commit messages:
```
feat: Add new Discord command for role management
fix: Resolve TTS synthesis timeout issue
docs: Update API documentation
test: Add tests for channel manager
refactor: Improve error handling in agent bot
```

## Pull Request Process

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests and linting**
   ```bash
   pytest
   flake8 .
   black .
   ```

3. **Push your changes**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create Pull Request**
   - Use a clear, descriptive title
   - Describe what changes you made and why
   - Reference any related issues
   - Include screenshots for UI changes
   - Ensure CI/CD checks pass

5. **Code Review**
   - Address reviewer feedback
   - Make requested changes
   - Keep discussion professional and constructive

## Areas for Contribution

### High Priority
- Bug fixes and stability improvements
- Performance optimizations
- Documentation improvements
- Test coverage expansion

### Feature Requests
- New Discord commands
- Additional AI personality types
- Enhanced monitoring features
- Integration with other services

### Good First Issues
Look for issues labeled `good-first-issue` for beginner-friendly contributions.

## Development Setup

### Required Environment Variables
```env
DISCORD_BOT_TOKEN=your_token
ANTHROPIC_API_KEY=your_key
GOOGLE_CLOUD_TTS_API_KEY=your_key
```

See `.env.example` for complete list.

### Running Locally
```bash
# Start the bot
python enhanced_agent_bot.py

# Run tests
pytest

# Run with debug logging
LOG_LEVEL=DEBUG python enhanced_agent_bot.py
```

## Reporting Bugs

When reporting bugs, include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Relevant logs or error messages
- Screenshots if applicable

## Feature Requests

When requesting features:
- Describe the feature clearly
- Explain the use case
- Provide examples if possible
- Consider implementation complexity
- Discuss potential alternatives

## Questions?

- Check existing documentation
- Search closed issues
- Ask in Discord server
- Create a discussion thread

## License

By contributing, you agree that your contributions will be licensed under the PROPRIETARY LICENSE
as specified in the LICENSE file. All contributions become the property of Andrew John Ward.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to Helix Unified! 🚀