# Native Installer Releases

## What Already Exists

This repository already contains the native installer path that should be used
as the fallback for non-technical users when Node/npm/npx are not available.

- `install.py` is the terminal installer and source-mode fallback.
- `install_gui.py` is the attorney-friendly GUI installer.
- `.github/workflows/build-release.yml` builds PyInstaller server binaries and
  GUI installers for many TasksAI verticals when a `v*` tag is pushed.
- The GitHub release process uploads the built installers as release assets.

## Current LawTasksAI Asset Names

The live `v2.1.0` release published on May 29, 2026 includes these LawTasksAI
assets:

```text
LawTasksAI-Setup.exe   Windows
LawTasksAI-Setup       macOS
```

`agent-install.json` must match those names exactly because AI assistants use
that manifest to decide what to download when `npx` is unavailable.

## Rules For Future Verticals

Do not add native fallback URLs to a vertical manifest until the release assets
exist and have been verified.

For a new vertical:

1. Add the vertical to the build matrix or create that vertical's release flow.
2. Publish a release with real Windows and macOS installer assets.
3. Verify the asset names through GitHub Releases.
4. Add the matching URLs to `agent-install.json`.
5. Update the vertical README to tell AI assistants whether native fallback is
   available.

Until step 3 is complete, the manifest should advertise only the `npx` path.

## Security Notes

The native installer may be downloaded or launched by an AI assistant, but the
user must approve OS prompts such as Windows SmartScreen, UAC, or macOS
security dialogs.

The installer must not be described as sending the user's task content to
LawTasksAI servers. LawTasksAI servers handle authentication, credits,
catalog/search metadata, and licensed skill delivery. The user's AI assistant
or LLM performs the task work according to that provider's privacy terms.
