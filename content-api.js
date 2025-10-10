// EdenTV Dynamic Content API
// Add this to make parts of your site update remotely

// Content storage (in production, use a database or Cloudflare KV)
let siteContent = {
    apps: [
        {
            id: 'parkmemoryhub',
            name: 'ParkMemoryHub',
            description: 'Advanced memory enhancement and cognitive training platform for iOS18.',
            status: 'Available on App Store',
            icon: '🧠'
        }
    ],
    contact: {
        email: 'contact@edentv.us',
        support: 'support@edentv.us'
    },
    stats: {
        apps: '1+',
        creativity: '∞',
        ios_version: 'iOS18'
    }
};

// API endpoint for content updates
async function handleContentRequest(request) {
    const url = new URL(request.url);

    if (request.method === 'GET') {
        // Return current content
        if (url.pathname === '/api/content') {
            return new Response(JSON.stringify(siteContent), {
                headers: { 'Content-Type': 'application/json' }
            });
        }
    }

    if (request.method === 'POST') {
        // Update content (add authentication in production!)
        if (url.pathname === '/api/content/update') {
            try {
                const updates = await request.json();
                siteContent = { ...siteContent, ...updates };
                return new Response(JSON.stringify({ success: true, content: siteContent }), {
                    headers: { 'Content-Type': 'application/json' }
                });
            } catch (error) {
                return new Response(JSON.stringify({ error: 'Invalid JSON' }), {
                    status: 400,
                    headers: { 'Content-Type': 'application/json' }
                });
            }
        }
    }

    return new Response('Not Found', { status: 404 });
}

// Export for Cloudflare Workers
export default {
    async fetch(request) {
        return handleContentRequest(request);
    }
};
