(function () {
    'use strict';

    var CONSENT_KEY = 'pulseCookieConsentV1';
    var OPTIONAL_KEYS = [
        'lightModeOn',
        'lightModeChoice',
        'lightDefaultMigratedV2',
        'lightPromptAnswered',
        'audioPlaybackSpeed',
        'audioFollowAlong',
        'readerFontScaleRate',
        'readerWideSpacing',
        'pulseViewHistory'
    ];
    var OPTIONAL_PREFIXES = ['liked_'];
    var FUNCTIONAL_KEYS = ['annEmail', 'my_comment_emails', 'pulseA11ySettingsV1', 'pulseA11ySettingsUpdatedAt'];
    var originalSetItem = null;
    var banner = null;
    var lastFocusedElement = null;

    function readChoice() {
        try {
            var value = window.localStorage.getItem(CONSENT_KEY);
            return value === 'all' || value === 'essential' || value === 'none' ? value : null;
        } catch (error) {
            return null;
        }
    }

    function isOptionalKey(key) {
        if (OPTIONAL_KEYS.indexOf(key) !== -1) return true;
        return OPTIONAL_PREFIXES.some(function (prefix) {
            return key.indexOf(prefix) === 0;
        });
    }

    function isFunctionalKey(key) {
        return FUNCTIONAL_KEYS.indexOf(key) !== -1;
    }

    function isBlockedKey(key) {
        var choice = readChoice();
        if (isOptionalKey(key)) return choice !== 'all';
        if (isFunctionalKey(key)) return choice !== 'all' && choice !== 'essential';
        return false;
    }

    function installStorageGuard() {
        try {
            originalSetItem = window.Storage.prototype.setItem;
            window.Storage.prototype.setItem = function (key, value) {
                try {
                    if (this === window.localStorage && isBlockedKey(String(key))) {
                        return;
                    }
                } catch (error) {
                    // Fall through to the original setter.
                }
                return originalSetItem.call(this, key, value);
            };
        } catch (error) {
            // Storage may be unavailable in private or restricted browsing modes.
        }
    }

    function clearStoredKeys(includeFunctional) {
        OPTIONAL_KEYS.forEach(function (key) {
            try { window.localStorage.removeItem(key); } catch (error) {}
        });
        if (includeFunctional) {
            FUNCTIONAL_KEYS.forEach(function (key) {
                try { window.localStorage.removeItem(key); } catch (error) {}
            });
        }
        try {
            var keys = [];
            for (var i = 0; i < window.localStorage.length; i += 1) {
                var key = window.localStorage.key(i);
                if (key && (isOptionalKey(key) || (includeFunctional && isFunctionalKey(key)))) keys.push(key);
            }
            keys.forEach(function (key) {
                try { window.localStorage.removeItem(key); } catch (error) {}
            });
        } catch (error) {}
    }

    function saveChoice(value) {
        try {
            window.localStorage.setItem(CONSENT_KEY, value);
        } catch (error) {
            return;
        }

        if (value === 'essential') clearStoredKeys(false);
        if (value === 'none') clearStoredKeys(true);

        try {
            window.dispatchEvent(new CustomEvent('pulse:cookie-consent', {
                detail: { choice: value }
            }));
        } catch (error) {}
    }

    function currentChoiceLabel() {
        var choice = readChoice();
        if (choice === 'all') return 'all optional preferences';
        if (choice === 'none') return 'no cookies';
        return 'essential storage only';
    }

    function isLightThemeContext() {
        try {
            if (document.body && document.body.classList.contains('light-mode')) return true;
            if (document.body && document.body.classList.contains('legal-page')) return true;
            return document.documentElement.getAttribute('data-theme') === 'light';
        } catch (error) {
            return false;
        }
    }

    function isGlobalFilterActive() {
        try {
            var filter = window.getComputedStyle(document.documentElement).filter;
            return !!filter && filter !== 'none';
        } catch (error) {
            return false;
        }
    }

    function syncBannerTheme() {
        if (!banner) return;
        banner.classList.toggle('pulse-cookie-banner-light', isLightThemeContext() && !isGlobalFilterActive());
    }

    function buildBanner() {
        if (banner) return banner;

        banner = document.createElement('section');
        banner.id = 'pulse-cookie-banner';
        banner.className = 'pulse-cookie-banner';
        banner.hidden = true;
        banner.setAttribute('role', 'dialog');
        banner.setAttribute('aria-modal', 'false');
        banner.setAttribute('aria-labelledby', 'pulse-cookie-title');
        banner.setAttribute('aria-describedby', 'pulse-cookie-copy pulse-cookie-links');
        banner.innerHTML = [
            '<h2 class="pulse-cookie-title" id="pulse-cookie-title">May we use cookies?</h2>',
            '<p class="pulse-cookie-copy" id="pulse-cookie-copy">We use essential cookies and local storage to keep the site secure and remember this choice. With permission, we also remember theme and reading preferences. No advertising cookies. Choose what you want to allow.</p>',
            '<p class="pulse-cookie-links" id="pulse-cookie-links"><a href="./privacy.html#cookies">Privacy Policy</a> <span aria-hidden="true">&middot;</span> <a href="./terms.html">Terms &amp; Conditions</a></p>',
            '<div class="pulse-cookie-actions">',
            '    <button type="button" class="pulse-cookie-btn pulse-cookie-btn-primary" data-cookie-choice="all">Allow cookies</button>',
            '    <button type="button" class="pulse-cookie-btn pulse-cookie-btn-secondary" data-cookie-choice="essential">Essential only</button>',
            '    <button type="button" class="pulse-cookie-btn pulse-cookie-btn-secondary" data-cookie-choice="none">No cookies</button>',
            '    <button type="button" class="pulse-cookie-btn pulse-cookie-btn-quiet" data-cookie-keep hidden>Keep current choice</button>',
            '</div>',
            '<p class="pulse-cookie-sr" aria-live="polite" data-cookie-status></p>'
        ].join('');

        banner.addEventListener('click', function (event) {
            var button = event.target.closest('[data-cookie-choice], [data-cookie-keep]');
            if (!button) return;

            if (button.hasAttribute('data-cookie-keep')) {
                hideBanner(!!lastFocusedElement);
                return;
            }

            saveChoice(button.getAttribute('data-cookie-choice'));
            hideBanner(!!lastFocusedElement);
        });

        banner.addEventListener('keydown', function (event) {
            if (event.key === 'Escape') {
                hideBanner(!!lastFocusedElement);
            }
        });

        document.body.appendChild(banner);
        return banner;
    }

    function showBanner(reopen) {
        var el = buildBanner();
        var existingChoice = readChoice();
        var keepButton = el.querySelector('[data-cookie-keep]');
        var status = el.querySelector('[data-cookie-status]');
        var copy = el.querySelector('#pulse-cookie-copy');

        if (existingChoice) {
            keepButton.hidden = false;
            copy.textContent = 'Your current choice is ' + currentChoiceLabel() + '. Essential storage keeps the site secure and remembers this choice. Optional storage remembers theme and reading preferences. No advertising cookies. You can change this anytime.';
        } else {
            keepButton.hidden = true;
            copy.textContent = 'We use essential cookies and local storage to keep the site secure and remember this choice. With permission, we also remember theme and reading preferences. No advertising cookies. Choose what you want to allow.';
        }

        el.hidden = false;
        syncBannerTheme();
        setTimeout(syncBannerTheme, 0);
        setTimeout(syncBannerTheme, 400);
        if (status) status.textContent = existingChoice ? 'Current choice: ' + currentChoiceLabel() + '.' : '';

        if (reopen) {
            lastFocusedElement = document.activeElement;
            var firstButton = el.querySelector('[data-cookie-choice="all"]');
            if (firstButton) firstButton.focus();
        }
    }

    function hideBanner(restoreFocus) {
        if (!banner) return;
        banner.hidden = true;
        if (!restoreFocus) return;

        if (lastFocusedElement && typeof lastFocusedElement.focus === 'function') {
            lastFocusedElement.focus();
        } else {
            var settingsButtons = document.querySelectorAll('[data-cookie-settings]');
            if (settingsButtons.length) settingsButtons[0].focus();
        }
        lastFocusedElement = null;
    }

    window.pulseOpenCookieSettings = function () {
        showBanner(true);
    };

    installStorageGuard();
    if (readChoice() === 'essential') clearStoredKeys(false);
    if (readChoice() === 'none') clearStoredKeys(true);

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            if (!readChoice()) showBanner(false);
        });
    } else if (!readChoice()) {
        showBanner(false);
    }

    document.addEventListener('click', function (event) {
        var trigger = event.target.closest('[data-cookie-settings]');
        if (!trigger) return;
        event.preventDefault();
        showBanner(true);
    });

    window.addEventListener('hashchange', syncBannerTheme);
    window.addEventListener('popstate', syncBannerTheme);
    if (typeof MutationObserver !== 'undefined' && document.body) {
        new MutationObserver(syncBannerTheme).observe(document.body, { attributes: true, subtree: true, attributeFilter: ['class'] });
    }
})();
