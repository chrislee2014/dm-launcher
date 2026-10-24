# Platform limits

Plan limits that matter at our scale (about 200 sites). Each entry gives its
source and how far to trust it.

## Sanity (blog CMS: one project per site, Free plan)

- **Number of projects:** no documented cap on Free plan projects.
  Source: https://www.sanity.io/answers/no-limit-to-free-plan-projects-on-sanity-io
  (updated 2025-12-01). Caveat: the answer there is labelled "AI Update", so
  it's community Q&A, not official policy. It suggests checking with Sanity
  billing support for any account-level limit that isn't public. Org-level
  limits aren't covered.
- **Per project (Free):** 20 users, 2 datasets, 2 roles, plus usage quotas
  (API requests, bandwidth, documents).
- **No overages on Free:** a project that exceeds its quotas can be
  **temporarily disabled**. For us, Sanity is read only at build time
  (`src/data/blog.ts`), so API usage per site should stay tiny. A site whose
  rebuild hook fires in a loop would be the risk.

## Cloudflare Workers Builds

- Unverified: from memory, the paid plan includes about 6,000 build minutes a
  month. Each site builds `main`, `staging` and `development` on every push.
  Check the current limit and our actual usage in the dashboard before relying
  on this.
