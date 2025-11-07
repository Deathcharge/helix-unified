# Contributing to the Helix Collective

First off, thank you for considering contributing to the Helix Collective. It's people like you that make the Helix Collective such a great community.

## Where do I go from here?

If you've noticed a bug or have a question, [search the issue tracker](https://github.com/Deathcharge/helix-unified/issues) to see if someone else has already created a ticket. If not, go ahead and [make one](https://github.com/Deathcharge/helix-unified/issues/new/choose)!

## Fork & create a branch

If this is something you think you can fix, then [fork the repository](https://github.com/Deathcharge/helix-unified/fork) and create a branch with a descriptive name.

A good branch name would be (where issue #325 is the ticket you're working on):

`git checkout -b 325-add-a-bug-fix`

## Get the test suite running

Make sure you're running the test suite locally before you make any changes.

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest
```

## Implement your fix or feature

At this point, you're ready to make your changes! Feel free to ask for help; everyone is a beginner at first :smile_cat:

## Make a Pull Request

At this point, you should switch back to your main branch and make sure it's up to date with the latest upstream changes.

```bash
git remote add upstream https://github.com/Deathcharge/helix-unified.git
git checkout main
git pull upstream main
```

Then, update your feature branch from your local copy of main, and push it!

```bash
git checkout 325-add-a-bug-fix
git rebase main
git push --force-with-lease origin 325-add-a-bug-fix
```

Finally, go to GitHub and [make a Pull Request](https://github.com/Deathcharge/helix-unified/compare)!

## Keeping your Pull Request updated

If a maintainer asks you to "rebase" your PR, they're saying that a lot of code has changed, and that you need to update your branch so it's easier to merge.

To learn more about rebasing and merging, check out [this guide](https://www.atlassian.com/git/tutorials/merging-vs-rebasing).

## Merging a PR (for maintainers)

A PR can only be merged into main by a maintainer if:

- It is passing CI.
- It has been approved by at least two maintainers.
- It has no requested changes.
- It is up to date with current main.

Any maintainer is allowed to merge a PR if all of these conditions are met.

## Shipping a release (for maintainers)

If you are a maintainer, you can ship a release by creating a new release on GitHub.

## That's it!

Thanks for being a part of the Helix Collective community!
