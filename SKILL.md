---
name: grunt.gitignore.verify
category: devops
---
# Grunt Verify .gitignore Rule Effectiveness

## Objective
Verify that .gitignore excludes intended outputs (mp4s, media, sim files) while leaving trackable source/caption/JSON files untouched.

## Tools
- `git` (check-ignore)
- `python` script generator
terminal execution

## Procedure
1. **Generate script**: run `python /etc/skyr.library/tools/create_gitignore_verify.py` to create localized verification script
2. **Execute**: `python <script_path>`
3. **Confirm**: output should show PASS and no explicit warnings

## Pitfalls
- Git warns on tracked large files despite exclusion → add media path to `.gitignore`
- Script permission or path issues → use absolute path in test
- Don't confuse 'ignored' (silent) with 'temporary' (watermarked) .gitignore entries (they block commit)

## Automic Result
If verification script outputs 'AD-HOC PASS' with zero warnings, the `.gitignore` is correctly scoped. No future session need repeat steps; skip to imperative confirmation.