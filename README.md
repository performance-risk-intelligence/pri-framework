# PRI public framework hub

A dependency-free, static HTML/CSS/JavaScript website for Performance Risk Intelligence. Public edition v0.4.1, prepared October 17, 2026. Repository publication and website deployment are separate steps; verify the Pages workflow before sharing a public website URL.

## Contents

- `index.html`: customer pain points and intended value, framework details, illustrative applications, proposed assessment and adoption phases, potential broader benefits, resources, and status.
- `roadmap.html`, `assessment.html`, `worked-example.html`, and `review-guide.html`: readable public planning briefs with downloadable Markdown versions.
- `assets/`: local styles, client-side interactions, and SVG favicon. No external fonts, tracking, forms, APIs, or analytics.
- `resources/`: public Markdown overview, three starter templates, evidence/value measurement note, and changelog.
- `.github/workflows/pages.yml`: GitHub Pages deployment workflow staging only the public site files.

The site is buildless. No package installation or external build script is needed.

## Local preview

From this directory, use an available static server, for example:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open the printed local address. Relative asset paths support a GitHub project-site subpath.

## Publication

Target repository: https://github.com/performance-risk-intelligence/pri-framework

Expected project-site URL after successful GitHub Pages configuration and deployment: https://performance-risk-intelligence.github.io/pri-framework/ (deployment verified October 17, 2026).

1. Review all public content, development-status descriptions, and downloads.
2. Use the dedicated target repository above, containing only this directory's public contents. Do not initialize or publish the surrounding document workspace. Preserve existing repository history and check for upstream changes before syncing.
3. Review account/organization identity and commit metadata if personal identity should not be public. A page without a biography does not make a repository owner anonymous.
4. Push the reviewed site to the repository's `main` branch.
5. Set Settings → Pages → Build and deployment → Source to GitHub Actions, then run or rerun the included workflow.
6. Verify the deployed URL and downloads before sharing. No custom domain, contact address, or public publication date is assumed here.

GitHub Pages is intended for static project sites and documentation and restricts use primarily directed at commercial transactions or providing commercial SaaS. This version is informational, with no booking, checkout, or commercial application. Reassess hosting if the site's purpose changes: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits

## Content maintenance

- Preserve PRI's four-pillar scope and incremental adoption model.
- Keep a genuine version/date trail. Update `resources/changelog.md`, the page's edition, and relevant resource versions together.
- Distinguish current resources, hypothetical demonstrations, planned capabilities, and measured/estimated/modeled results.
- Do not imply validation, adoption, partnerships, endorsements, or results without evidence and permission.
- The interaction is a synthetic rules-based illustration. It never approves a production release or represents a predictive engine.
- The starter templates are newly authored resources, not validated operating controls.
- Keep personal information, biographies, resumes, private correspondence, employer materials, and customer identities out of the public site unless explicitly approved.
- The repository's presence does not imply an open-source license grant. Choose a license deliberately before offering reuse rights beyond sharing the materials for evaluation.

## First-edition scope

This edition supplies a methodology overview and starter resources. It does not implement PRI's predictive models, integrations, commercial operations, or production validation. Energy-impact modeling remains planned. The broader evidence-pack workstream continues separately.
