<!--
  generic-project-design | design/initial-concept/docs/07-instantiation-checklist.md
-->

# 07 — Instantiation: copy → rename → publish

The requirement: copy the parent folder, delete the design folder, name the
project, push two repos. This is what has to be true for that to be
mechanical rather than a careful manual edit.

---

## 1. The placeholder-token contract

**The single biggest risk is a half-renamed template** — the string `generic`
surviving in 40 files, some of them inside prose where it reads as a normal
English word. Substituting a bare word like `generic` with `sed` is exactly
how that happens.

So the template must never contain the bare word as a name. It uses tokens:

| Token | Becomes | Example |
|---|---|---|
| `{{PROJECT}}` | the product repo / project name | `strategy-lab-console` |
| `{{PROJECT_TITLE}}` | human title | `Strategy-Lab Console` |
| `{{FAMILY}}` | the family / parent stem | `strategy-lab` |
| `{{DEV_REPO}}` | `{{PROJECT}}-dev` | `strategy-lab-console-dev` |
| `{{GITHUB_ORG}}` | org or user | `Strategy-Team` |
| `{{DATE}}` | instantiation date | `2026-08-18` |

Rules that make this safe:

1. **No unbraced placeholder text anywhere.** Directory names too — ship the
   dirs as `{{PROJECT}}/` and `{{PROJECT}}-dev/` rather than `generic/`.
   *(The folders created today are `generic/` and `generic-dev/` as you
   specified; converting them to token form is part of the first build
   session — see the note in §5.)*
2. **A `template.yml` manifest** at the parent listing every token, its
   description, and a validation regex.
3. **`init.sh` does the substitution**, and then **greps for surviving
   `{{`** and fails loudly if any remain. A rename that half-succeeds is
   worse than one that refuses.

## 2. The sequence

```bash
# 1. copy the parent (never move — the template stays pristine)
cp -r /workspaces/generic-project /workspaces/{{FAMILY}}-suite

# 2. drop the scaffolding conversation
rm -rf /workspaces/{{FAMILY}}-suite/generic-project-design

# 3. name it — substitutes tokens, renames dirs, then verifies none remain
cd /workspaces/{{FAMILY}}-suite && ./init.sh \
    --project my-thing --family my-family --org MyOrg

# 4. two independent repos, two initial commits
(cd my-thing     && git init && git add -A && git commit -m "Initial scaffold from template vX.Y")
(cd my-thing-dev && git init && git add -A && git commit -m "Initial scaffold from template vX.Y")

# 5. publish
gh repo create MyOrg/my-thing     --private --source=my-thing     --push
gh repo create MyOrg/my-thing-dev --private --source=my-thing-dev --push

# 6. prove the invariants hold on an empty project
(cd my-thing && ./scripts/check-governance.sh)   # must pass on a fresh instance
```

`init.sh` deletes itself and `template.yml` on success — the instantiated
project should carry no template machinery.

## 3. Ordering that matters

- **Delete the design folder before `git init`**, or the scaffolding
  conversation lands in the product's history permanently.
- **`git init` per child, never at the parent.** The parent is a container
  and must have no `.git`. Worth a check in `init.sh`.
- **Both repos get their first commit before either is pushed**, so the
  cross-repo `SYNC.yml` pins reference real commits rather than being
  back-filled.
- **Run the check suite on the empty instance (step 6).** If the invariants
  cannot pass on a fresh scaffold, they will never pass again.

## 4. What the fresh instance must contain

Non-negotiable, or the first session improvises and the template's whole
point is lost:

- `{{PROJECT}}/CLAUDE.md` — filled in, under budget, zero mutable state, and
  pointing at the dev repo for protocol and queue.
- `{{PROJECT}}-dev/README.md` — first line defines what the repo is *not*.
- `{{PROJECT}}-dev/PROTOCOL.md` — the session protocol.
- `{{PROJECT}}-dev/QUEUE.md` — generated, legitimately empty, present.
- `governance/units/_TEMPLATE.md` and one worked example.
- `issues/README.md` — the issue type/routing rule, with zero records.
- `scripts/check-governance.*` — **passing**.
- `TEMPLATE_VERSION` — so D-05's drift check has something to compare.

An empty-but-correct scaffold is the deliverable. A scaffold full of
`TODO: decide this` is how a template teaches an agent that its own rules are
optional.

## 5. Note on the folders created today

`generic/` and `generic-dev/` exist and are intentionally empty. They are
placeholders for the shape argued in
[`05-proposed-structure.md`](05-proposed-structure.md), not the shape itself
— populating them before
[`06-open-questions.md`](06-open-questions.md) D-01…D-04 are answered would
bake in decisions this conversation exists to make.

The conversion to `{{PROJECT}}/` token-form directory names happens in the
same session that populates them.
