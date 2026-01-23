#!/usr/bin/env node

/**
 * Google Passkey Disabler - FULLY AUTOMATED with 1Password
 *
 * Uses 1Password CLI to retrieve credentials and fully automates
 * the process of disabling Google's passkey requirement.
 */

const puppeteer = require('puppeteer');
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Configuration
const GOOGLE_EMAIL = 'mike.finneran@gmail.com';
const SCREENSHOT_DIR = path.join(__dirname, 'google-passkey-screenshots');
const HEADLESS = false; // Set to true for background execution

// Create screenshot directory
if (!fs.existsSync(SCREENSHOT_DIR)) {
    fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

function log(message, type = 'info') {
    const timestamp = new Date().toISOString();
    const icons = {
        info: 'ℹ️',
        success: '✅',
        error: '❌',
        warning: '⚠️',
        step: '🔧'
    };
    console.log(`${icons[type]} [${timestamp}] ${message}`);
}

async function getGooglePassword() {
    try {
        log('Retrieving Google password from 1Password...', 'step');

        // Try to get the password from 1Password
        const password = execSync(
            `op item get Google --fields password`,
            { encoding: 'utf-8' }
        ).trim();

        if (!password) {
            throw new Error('No password retrieved from 1Password');
        }

        log('Password retrieved successfully', 'success');
        return password;
    } catch (error) {
        log(`Failed to retrieve password: ${error.message}`, 'error');
        log('Make sure 1Password CLI is authenticated (run: op signin)', 'warning');
        throw error;
    }
}

async function takeScreenshot(page, name) {
    const screenshotPath = path.join(SCREENSHOT_DIR, `${Date.now()}-${name}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: true });
    log(`Screenshot saved: ${name}`, 'info');
    return screenshotPath;
}

async function waitForNavigation(page, timeout = 30000) {
    try {
        await page.waitForNavigation({ waitUntil: 'networkidle2', timeout });
    } catch (error) {
        log('Navigation wait timed out (may be okay)', 'warning');
    }
}

async function loginToGoogle(page, password) {
    log('Navigating to Google Account Security...', 'step');
    await page.goto('https://myaccount.google.com/security', {
        waitUntil: 'networkidle2'
    });

    await page.waitForTimeout(2000);
    await takeScreenshot(page, '1-initial-page');

    // Check if we need to log in
    const currentUrl = page.url();
    if (currentUrl.includes('accounts.google.com')) {
        log('Login required, entering credentials...', 'step');

        // Enter email
        const emailSelectors = [
            'input[type="email"]',
            '#identifierId',
            'input[name="identifier"]'
        ];

        for (const selector of emailSelectors) {
            try {
                await page.waitForSelector(selector, { timeout: 5000 });
                await page.type(selector, GOOGLE_EMAIL, { delay: 100 });
                log('Email entered', 'success');
                await takeScreenshot(page, '2-email-entered');

                // Click Next
                await page.keyboard.press('Enter');
                await page.waitForTimeout(3000);
                await takeScreenshot(page, '3-after-email-next');
                break;
            } catch (error) {
                continue;
            }
        }

        // Enter password
        const passwordSelectors = [
            'input[type="password"]',
            '#password input',
            'input[name="password"]'
        ];

        for (const selector of passwordSelectors) {
            try {
                await page.waitForSelector(selector, { timeout: 10000 });
                await page.type(selector, password, { delay: 100 });
                log('Password entered', 'success');
                await takeScreenshot(page, '4-password-entered');

                // Click Next/Sign in
                await page.keyboard.press('Enter');
                await page.waitForTimeout(5000);
                await takeScreenshot(page, '5-after-password-submit');
                break;
            } catch (error) {
                continue;
            }
        }

        // Wait for potential 2FA or redirect to security page
        await page.waitForTimeout(5000);
        const finalUrl = page.url();

        if (finalUrl.includes('challenge') || finalUrl.includes('2fa') || finalUrl.includes('verification')) {
            log('2FA required - please complete on your device', 'warning');
            log('Waiting 60 seconds for 2FA completion...', 'info');
            await page.waitForTimeout(60000);
            await takeScreenshot(page, '6-after-2fa');
        }

        // Navigate to security page after login
        await page.goto('https://myaccount.google.com/security', {
            waitUntil: 'networkidle2'
        });
        await page.waitForTimeout(2000);
    }

    log('Logged in to Google Account', 'success');
    await takeScreenshot(page, '7-logged-in');
}

async function disableSkipPassword(page) {
    log('Disabling "Skip password when possible"...', 'step');

    await takeScreenshot(page, '8-before-disable');

    const skipPasswordSelectors = [
        'text/Skip password when possible',
        'aria/Skip password when possible',
        '[data-skip-password]',
        'div:contains("Skip password")'
    ];

    try {
        // Try to find and click the skip password option
        let clicked = false;

        // Method 1: Look for text content
        const elements = await page.$$('*');
        for (const element of elements) {
            try {
                const text = await page.evaluate(el => el.textContent, element);
                if (text && text.includes('Skip password when possible')) {
                    await element.click();
                    clicked = true;
                    log('Found and clicked skip password option', 'success');
                    break;
                }
            } catch (error) {
                continue;
            }
        }

        if (!clicked) {
            log('Could not find skip password option automatically', 'warning');
            log('You may need to manually disable it', 'warning');
            return false;
        }

        await page.waitForTimeout(2000);
        await takeScreenshot(page, '9-skip-password-clicked');

        // Look for toggle to turn OFF
        const toggleSelectors = [
            '[role="switch"]',
            'input[type="checkbox"]',
            '[aria-checked="true"]'
        ];

        for (const selector of toggleSelectors) {
            try {
                const toggle = await page.$(selector);
                if (toggle) {
                    const isChecked = await page.evaluate(
                        el => el.getAttribute('aria-checked') === 'true' || el.checked,
                        toggle
                    );

                    if (isChecked) {
                        await toggle.click();
                        log('Disabled skip password toggle', 'success');
                        await page.waitForTimeout(2000);
                        await takeScreenshot(page, '10-toggle-disabled');
                        return true;
                    }
                }
            } catch (error) {
                continue;
            }
        }

        log('Toggle state unclear, check screenshots', 'warning');
        return false;
    } catch (error) {
        log(`Error disabling skip password: ${error.message}`, 'error');
        return false;
    }
}

async function deleteAllPasskeys(page) {
    log('Navigating to passkeys page...', 'step');

    await page.goto('https://myaccount.google.com/signinoptions/passkeys', {
        waitUntil: 'networkidle2'
    });
    await page.waitForTimeout(3000);
    await takeScreenshot(page, '11-passkeys-page');

    let deletedCount = 0;
    let attempts = 0;
    const maxAttempts = 20; // Safety limit

    while (attempts < maxAttempts) {
        attempts++;

        try {
            // Look for delete/remove buttons
            const deleteSelectors = [
                '[aria-label*="Remove"]',
                '[aria-label*="Delete"]',
                'button:contains("Remove")',
                'button:contains("Delete")',
                '[data-action="remove"]'
            ];

            let deleteButton = null;

            // Try each selector
            for (const selector of deleteSelectors) {
                try {
                    deleteButton = await page.$(selector);
                    if (deleteButton) break;
                } catch (error) {
                    continue;
                }
            }

            // Also try finding by text content
            if (!deleteButton) {
                const buttons = await page.$$('button');
                for (const button of buttons) {
                    const text = await page.evaluate(el => el.textContent, button);
                    if (text && (text.includes('Remove') || text.includes('Delete'))) {
                        deleteButton = button;
                        break;
                    }
                }
            }

            if (!deleteButton) {
                log(`No more passkeys found to delete (checked ${deletedCount} times)`, 'info');
                break;
            }

            // Click delete button
            await deleteButton.click();
            await page.waitForTimeout(1000);

            // Look for confirmation button
            const confirmSelectors = [
                'button:contains("Remove")',
                'button:contains("Confirm")',
                'button:contains("Delete")',
                '[data-action="confirm"]'
            ];

            let confirmed = false;
            for (const selector of confirmSelectors) {
                try {
                    const confirmButton = await page.$(selector);
                    if (confirmButton) {
                        await confirmButton.click();
                        confirmed = true;
                        break;
                    }
                } catch (error) {
                    continue;
                }
            }

            if (!confirmed) {
                // Try finding confirm button by text
                const buttons = await page.$$('button');
                for (const button of buttons) {
                    const text = await page.evaluate(el => el.textContent, button);
                    if (text && (text.includes('Remove') || text.includes('Confirm') || text.includes('Delete'))) {
                        await button.click();
                        confirmed = true;
                        break;
                    }
                }
            }

            deletedCount++;
            log(`Deleted passkey ${deletedCount}`, 'success');

            await page.waitForTimeout(2000);
            await takeScreenshot(page, `12-deleted-passkey-${deletedCount}`);

        } catch (error) {
            log(`Error during passkey deletion: ${error.message}`, 'warning');
            break;
        }
    }

    await takeScreenshot(page, '13-all-passkeys-deleted');
    log(`Total passkeys deleted: ${deletedCount}`, 'success');

    return deletedCount;
}

async function main() {
    console.log('\n╔════════════════════════════════════════════════════════════════╗');
    console.log('║     Google Passkey Disabler - FULLY AUTOMATED with 1Password  ║');
    console.log('╚════════════════════════════════════════════════════════════════╝\n');

    let browser;
    let password;

    try {
        // Get password from 1Password
        password = await getGooglePassword();

        // Launch browser
        log('Launching browser...', 'step');
        browser = await puppeteer.launch({
            headless: HEADLESS,
            defaultViewport: { width: 1280, height: 800 },
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-blink-features=AutomationControlled'
            ]
        });

        const page = await browser.newPage();

        // Set realistic user agent
        await page.setUserAgent(
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        );

        // Login
        await loginToGoogle(page, password);

        // Disable skip password
        await disableSkipPassword(page);

        // Delete passkeys
        const deletedCount = await deleteAllPasskeys(page);

        // Final verification screenshot
        await page.goto('https://myaccount.google.com/security', {
            waitUntil: 'networkidle2'
        });
        await page.waitForTimeout(2000);
        await takeScreenshot(page, '14-final-security-page');

        console.log('\n╔════════════════════════════════════════════════════════════════╗');
        console.log('║                     Fix Complete!                              ║');
        console.log('╚════════════════════════════════════════════════════════════════╝\n');
        console.log(`✅ Passkeys deleted: ${deletedCount}`);
        console.log(`📁 Screenshots saved to: ${SCREENSHOT_DIR}`);
        console.log('\n✅ Your Google account should now use password login instead of passkeys');
        console.log('✅ Test by signing out and signing back in\n');

    } catch (error) {
        log(`Fatal error: ${error.message}`, 'error');
        console.error(error);
        process.exit(1);
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}

// Run the script
main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
});
