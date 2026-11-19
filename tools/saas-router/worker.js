// Router for client domains whose DNS stays outside our Cloudflare account
// (Cloudflare for SaaS on dentalmarketing.com, fallback origin sites.dentalmarketing.com).
// Route */* sends every custom hostname here; *dentalmarketing.com/* is excluded by a
// Worker-less route. Unknown hostnames get a 404, never another client's site.
// To add a client: add the hostname below and a service binding to its site Worker.
const SITES = {
  "www.robinwoodsmiles.com": "ROBINWOODSMILES",
};

export default {
  async fetch(request, env) {
    const host = new URL(request.url).hostname.toLowerCase();
    const binding = SITES[host];
    if (binding && env[binding]) return env[binding].fetch(request);
    return new Response("Not found", { status: 404, headers: { "content-type": "text/plain" } });
  },
};
