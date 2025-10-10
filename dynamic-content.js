// Dynamic Content Loader for EdenTV
// Add this to your main script.js to load content dynamically

class DynamicContentLoader {
    constructor() {
        this.contentCache = {};
        this.apiEndpoint = '/api/content'; // This would be your Cloudflare Worker endpoint
    }

    // Load content from API
    async loadContent() {
        try {
            const response = await fetch(this.apiEndpoint);
            const data = await response.json();
            this.contentCache = data;
            this.updatePageContent(data);
        } catch (error) {
            console.log('Using static content (API not available)', error);
        }
    }

    // Update page content with dynamic data
    updatePageContent(data) {
        // Update app information
        if (data.apps) {
            data.apps.forEach(app => {
                const appElement = document.querySelector(`[data-app-id="${app.id}"]`);
                if (appElement) {
                    appElement.querySelector('h3').textContent = app.name;
                    appElement.querySelector('p').textContent = app.description;
                    appElement.querySelector('.app-icon').textContent = app.icon;
                }
            });
        }

        // Update contact information
        if (data.contact) {
            const contactElements = document.querySelectorAll('[data-contact]');
            contactElements.forEach(element => {
                const type = element.getAttribute('data-contact');
                if (data.contact[type]) {
                    element.textContent = data.contact[type];
                    element.href = `mailto:${data.contact[type]}`;
                }
            });
        }

        // Update stats
        if (data.stats) {
            Object.keys(data.stats).forEach(key => {
                const statElement = document.querySelector(`[data-stat="${key}"]`);
                if (statElement) {
                    statElement.textContent = data.stats[key];
                }
            });
        }
    }

    // Update content via API (for admin use)
    async updateContent(updates, apiKey) {
        try {
            const response = await fetch('/api/content/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiKey}`
                },
                body: JSON.stringify(updates)
            });

            const result = await response.json();
            if (result.success) {
                this.loadContent(); // Refresh the page content
                return { success: true };
            }
            return { error: result.error };
        } catch (error) {
            return { error: error.message };
        }
    }
}

// Initialize dynamic content loading
document.addEventListener('DOMContentLoaded', () => {
    const contentLoader = new DynamicContentLoader();
    contentLoader.loadContent();

    // Make it globally available for admin updates
    window.edentvContent = contentLoader;
});

// Admin update function (call this from browser console or admin panel)
/*
window.edentvContent.updateContent({
    apps: [{
        id: 'parkmemoryhub',
        name: 'ParkMemoryHub Pro',
        description: 'Enhanced version with new AI features',
        icon: '🧠'
    }]
}, 'your-api-key');
*/
