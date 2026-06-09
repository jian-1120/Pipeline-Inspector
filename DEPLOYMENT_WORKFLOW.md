# Deployment Workflow

Purpose: keep Blender runtime code in sync with the repository source during Pipeline Inspector runtime validation.

## Current Problem

Repository source lives at:

`C:\Users\简某\Desktop\AI\Pipeline Inspector总\Pipeline-Inspector\pipeline_inspector`

Blender 5.1.1 runtime loads add-ons from:

`C:\Users\简某\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\pipeline_inspector`

These are separate directories.

Installing a zip into Blender copies the add-on into the Blender user add-ons directory. After that copy is made, later repository changes do not automatically update Blender's installed runtime copy.

This caused Blender to execute stale Check04 placeholder code while the repository already contained the real Check04 implementation.

## Audit Findings

Before deployment sync:

- Repository `pipeline_inspector/checks/uvs.py`
  - Size: `4692` bytes
  - SHA256: `e0ee9e5da91c6101fd17d52addb699f415cdb838df369db57b5049481df3f42e`
  - Contains `def uv_status`
  - Contains `base.make_fail`
- Blender runtime `pipeline_inspector/checks/uvs.py`
  - Size: `281` bytes
  - SHA256: `d0e333a416ecfb2902c3cb01460f2a3de7d7a0486bde80103a3d9ba94a210c72`
  - Contains scaffold placeholder logic
  - Always returned PASS
- Current zip package also contained stale placeholder Check04 code, so rebuilding or reinstalling from that zip would not fix runtime consistency unless the zip was rebuilt first.

## Options Considered

### A. Rebuild and reinstall add-on zip

Good for release packaging and user installation testing.

Risk for runtime validation:

- Creates a frozen snapshot.
- Easy to forget rebuilding the zip after source changes.
- Blender can keep running old installed files if reinstall is skipped or install cache is stale.

### B. Direct sync repository to Blender add-ons folder

Chosen workflow.

Why:

- Simple and explicit.
- No admin permissions required.
- Avoids symlink and junction edge cases.
- Makes Blender's runtime files byte-for-byte match the repository source.
- Best fit for current development and runtime validation work.

### C. Junction or symbolic link

Not chosen.

Why:

- More fragile on Windows.
- May require elevated permissions depending on system policy.
- Blender and packaging tests can behave differently with linked folders.
- Harder to rollback cleanly for non-technical operators.

## Chosen Solution

Use direct sync from the repository add-on folder into Blender's user add-ons folder.

Source:

`C:\Users\简某\Desktop\AI\Pipeline Inspector总\Pipeline-Inspector\pipeline_inspector`

Destination:

`C:\Users\简某\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\pipeline_inspector`

The sync mirrors the source folder into the runtime folder and excludes Python cache files.

## Exact Deployment Steps

Run from the project root:

`C:\Users\简某\Desktop\AI\Pipeline Inspector总\Pipeline-Inspector`

PowerShell command:

```powershell
$repo = "C:\Users\简某\Desktop\AI\Pipeline Inspector总\Pipeline-Inspector"
$src = Join-Path $repo "pipeline_inspector"
$dst = "C:\Users\简某\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\pipeline_inspector"

if (!(Test-Path -LiteralPath $src)) {
    throw "Source missing: $src"
}

if (!(Test-Path -LiteralPath (Split-Path -Parent $dst))) {
    throw "Blender add-ons parent missing: $(Split-Path -Parent $dst)"
}

if ((Resolve-Path -LiteralPath $src).Path -eq (Resolve-Path -LiteralPath $dst).Path) {
    throw "Source and destination are the same path; aborting."
}

robocopy $src $dst /MIR /XD __pycache__ /XF *.pyc

if ($LASTEXITCODE -gt 7) {
    throw "robocopy failed with exit code $LASTEXITCODE"
}
```

Notes:

- `robocopy` exit codes `0` through `7` are non-fatal.
- `/MIR` makes the Blender runtime folder match the repository add-on folder.
- `/XD __pycache__` and `/XF *.pyc` prevent cache artifacts from becoming part of the runtime deployment.

## Rollback Steps

Rollback option 1: reinstall a known-good zip through Blender.

1. Open Blender.
2. Go to `Edit > Preferences > Add-ons`.
3. Disable and remove `Pipeline Inspector`.
4. Install the known-good zip.
5. Enable `Pipeline Inspector`.
6. Run the verification steps below.

Rollback option 2: restore runtime files from Git source.

1. Check out the desired commit in the repository.
2. Run the direct sync deployment command again.
3. Run the verification steps below.

Do not manually edit files inside Blender's add-ons folder.

## Verification Steps

### 1. Verify file hash match

PowerShell:

```powershell
$repoUvs = "C:\Users\简某\Desktop\AI\Pipeline Inspector总\Pipeline-Inspector\pipeline_inspector\checks\uvs.py"
$runtimeUvs = "C:\Users\简某\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\pipeline_inspector\checks\uvs.py"

Get-FileHash -LiteralPath $repoUvs -Algorithm SHA256
Get-FileHash -LiteralPath $runtimeUvs -Algorithm SHA256
```

Expected:

- Both SHA256 hashes are identical.

Current verified hash after sync:

`e0ee9e5da91c6101fd17d52addb699f415cdb838df369db57b5049481df3f42e`

### 2. Verify Blender loaded source path

Run Blender in background with a Python audit script that imports:

```python
import pipeline_inspector
from pipeline_inspector.checks import uvs

print(pipeline_inspector.__file__)
print(uvs.__file__)
print(hasattr(uvs, "uv_status"))
print(hasattr(uvs, "degenerate_active_status"))
```

Expected:

- `pipeline_inspector.__file__` points to Blender's user add-ons directory.
- `uvs.__file__` points to:

`C:\Users\简某\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\pipeline_inspector\checks\uvs.py`

- `uv_status`: `True`
- `degenerate_active_status`: `True`

### 3. Verify Check04 runtime behavior

Create a mesh with no UV maps and run:

```python
bpy.ops.pipeline_inspector.run()
```

Expected Check04 result:

- Status: `FAIL`
- Message: `1 object(s) have no usable UV map: Cube_No_UV.`
- Affected objects: `Cube_No_UV`

Current verification after sync:

- Blender version: `5.1.1`
- Loaded `uvs.py`: Blender user add-ons path
- Loaded `uvs.py` size: `4692` bytes
- Loaded `uvs.py` SHA256: `e0ee9e5da91c6101fd17d52addb699f415cdb838df369db57b5049481df3f42e`
- `uv_status`: present
- `degenerate_active_status`: present
- No-UV smoke test: `FAIL`
- Message: `1 object(s) have no usable UV map: Cube_No_UV.`

## Operating Rule

Before any Blender runtime validation:

1. Pull or confirm the repository source is current.
2. Run the direct sync deployment command.
3. Verify the runtime file hash matches the repository file hash.
4. Start Blender and run the validation scenario.

For release packaging tests, rebuild the zip separately and verify its internal source files before installing it. Do not use the zip as the default development deployment path.
