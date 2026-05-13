/**
 * Tatle tale Website Polish & Interactions
 */
document.addEventListener('DOMContentLoaded', function() {
    initMobileMenuFix();
    fixNavbarLinks();
});

/**
 * Ensure mobile menu works correctly and closes on link click
 */
function initMobileMenuFix() {
    const overlay = document.getElementById('tt-mobile-menu-overlay');
    if (!overlay) return;

    const navLinks = overlay.querySelectorAll('a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            overlay.classList.remove('open');
            document.body.style.overflow = '';
        });
    });
}

/**
 * Surgical fix for navbar links if they are still using Wix format
 */
function fixNavbarLinks() {
    const links = document.querySelectorAll('a[data-testid="linkElement"], .wixui-horizontal-menu__item-link');
    links.forEach(link => {
        const href = link.getAttribute('href');
        if (!href) return;

        // Clean up Wix URLs
        if (href.includes('turtle-tales-story')) link.setAttribute('href', '/turtle-tales-story');
        if (href.includes('workshop-chapters')) link.setAttribute('href', '/workshop-chapters');
        if (href.includes('community-survey')) link.setAttribute('href', '/survey');
        if (href.includes('about-lana')) link.setAttribute('href', '/about-lana');
        if (href === '/index.html' || href === 'index.html') link.setAttribute('href', '/');
    });
}
