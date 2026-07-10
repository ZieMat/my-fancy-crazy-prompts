# Installing grok-build-setup

## Global install (recommended)

Copy or symlink the skill into your user skills directory:

```bash
cp -r /path/to/grok-build-setup ~/.grok/skills/
# or
ln -s /path/to/grok-build-setup ~/.grok/skills/grok-build-setup
```

## Verify

```bash
grok inspect
```

Look for `grok-build-setup` in the Skills section.

## Usage

In any project directory:

```
/grok-build-setup
/grok-build-setup node
/grok-build-setup --merge python
```

## Uninstall

```bash
rm -rf ~/.grok/skills/grok-build-setup
```