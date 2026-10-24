# dm-launcher

How we launch Dental Marketing client sites (Astro, built from the website
starter template) onto Cloudflare Workers, moving them off Webflow, and
what has gone wrong along the way.

- [RUNBOOK.md](RUNBOOK.md): the cutover, step by step.
- [PITFALLS.md](PITFALLS.md): things that bit us, and how to catch them.
- [sites/](sites/): one log per launched site (state before, what was
  done, verification results).

Cloudflare account: **Dental Marketing**. Each client domain is a zone in
that account. Each site is a Worker named after the domain
(`smilesofpensacola-com`), built by Workers Builds from the client repo:
`main` → production, `staging` → `staging-<worker>.dental-marketing.workers.dev`.
