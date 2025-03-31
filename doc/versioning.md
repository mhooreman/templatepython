# Versioning

[Semantic versioning](https://semver.org/) is used:

- Versions are based on three positive numbers and an optional suffix separated
  by a dot. For example `0.0.1.dev3`, or `1.2.3`.
- The first number is the *major*. It changes when major changes are
  applied. They can break compatibility with previous versions.
- The second number is the *minor*. It changes when there are some new
  features or changes in existing features.
- The third number is the *patch*. It changes when there are only bug
  fixes.
- For the *suffix*:
    - `dev` followed by a number is a development release, it comes prior to the
      release
    - `rc`, `alpha` or `beta` followed by a number is respectively an release
      candidate, alpha or beta release; it comes prio to the release

Versions are associated with milestones. A milestone is a version number
*without suffix*:

- Development items (e.g. GitHub tickets, see [development](development.md))
  are associated to those milestones
- The releases, change logs and source code tags and branches are associated to
  the versions including the potential suffixes.

In terms of (increasing) maturity level:

- Pre-alpha versions can only be used in development environment, for
  development purpuse.
- Alpha versions can only be used in development environment, for testing
  purposes.
- Beta version can only be used in validation environment.
- Production versions can be used in operations/production environment.
- Release candidates have no defined rule can shall be avoided.

Versus version numbers:

- Versions with `dev` suffix are always pre-alpha.
- Versions with `alpha` suffix are always alpha.
- Versions with `beta` suffix are always beta.
- Versions with `rc` shall be avoided.
- Versions `0.0.x` are alpha.
- Versions from `0.1.x` and before `1.0.0` excluded are beta.
- Versions from `1.0.0` are production.
