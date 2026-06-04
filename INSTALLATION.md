# Installation

Current version: **Scaffold / Early Prototype**

This installation process is only for Blender add-on loading tests. The current version is not a usable product and must not be used for real delivery judgment.

## Install For Load Testing

1. Create a zip file containing the `pipeline_inspector/` folder.
2. Open Blender.
3. Go to `Edit > Preferences > Add-ons`.
4. Click `Install`.
5. Select the zip file.
6. Enable `Pipeline Inspector`.

## Current Expected Result

The add-on is expected to load as a scaffold and expose the basic registration shell.

The current five checks are placeholders:

1. Texture Presence
2. Material Assignment
3. Applied Scale
4. UV Existence
5. Normal Consistency

They do not yet perform real checks.

## Important Warning

Do not use the current version to decide whether a Blender asset is ready for delivery.

The current version is only for:

- packaging test
- install test
- enable/disable test
- early Blender runtime load test

It is not ready for:

- real asset inspection
- marketplace submission decisions
- client delivery decisions
- production use
