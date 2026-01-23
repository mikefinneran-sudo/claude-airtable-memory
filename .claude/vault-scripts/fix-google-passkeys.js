/**
 * Google Passkey Disabler
 * Automates disabling "Skip password when possible" and deleting all passkeys
 *
 * Usage: node fix-google-passkeys.js
 *
 * Requirements: npm install puppeteer
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Create screenshots directory
const screenshotsDir = path.join(__dirname, 'google-passkey-screenshots');
if (!fs.existsSync(screenshotsDir)) {
  fs.mkdirSync(screenshotsDir);
}

async function screenshot(page, name) {
  const filepath = path.join(screenshotsDir, `${Date.now()}-${name}.png`);
  await page.screenshot({ path: filepath, fullPage: true });
  console.log(`📸 Screenshot saved: ${filepath}`);
  return filepath;
}

async function waitForNavigation(page, timeout = 10000) {
  try {
    await page.waitForNavigation({ waitUntil: 'networkidle2', timeout });
  } catch (error) {
    console.log('⏳ Navigation timeout (page may have loaded anyway)');
  }
}

async function disablePasskeyRequirement(page) {
  console.log('\n🔧 Step 1: Disabling "Skip password when possible" setting...');

  // Navigate to security settings
  await page.goto('https://myaccount.google.com/security', { waitUntil: 'networkidle2' });
  await page.waitForTimeout(3000);
  await screenshot(page, 'security-page');

  // Look for "Skip password when possible" toggle
  const selectors = [
    'div[data-rid="skip-password"]',
    'div[aria-label*="Skip password"]',
    'div[aria-label*="passkey"]',
    'c-wiz[data-node-index] div[role="switch"]',
    'div[role="switch"][aria-checked="true"]'
  ];

  let toggleFound = false;

  for (const selector of selectors) {
    try {
      await page.waitForSelector(selector, { timeout: 5000 });
      const elements = await page.$$(selector);

      for (const element of elements) {
        const text = await page.evaluate(el => el.textContent, element);

        if (text.toLowerCase().includes('skip password') ||
            text.toLowerCase().includes('passkey')) {

          // Check if it's currently enabled
          const ariaChecked = await page.evaluate(el => el.getAttribute('aria-checked'), element);

          if (ariaChecked === 'true') {
            console.log('✅ Found "Skip password when possible" toggle - it is ON');
            await element.click();
            await page.waitForTimeout(2000);
            await screenshot(page, 'toggle-clicked');

            // Verify it's now off
            const newState = await page.evaluate(el => el.getAttribute('aria-checked'), element);
            if (newState === 'false') {
              console.log('✅ Successfully disabled "Skip password when possible"');
              toggleFound = true;
              break;
            }
          } else {
            console.log('ℹ️  "Skip password when possible" is already OFF');
            toggleFound = true;
            break;
          }
        }
      }

      if (toggleFound) break;
    } catch (error) {
      // Try next selector
      continue;
    }
  }

  if (!toggleFound) {
    console.log('⚠️  Could not find "Skip password when possible" toggle automatically');
    console.log('📋 Please manually disable it on this page');
    await screenshot(page, 'manual-toggle-needed');

    // Wait for user to do it manually
    console.log('\n⏸️  Press ENTER after you have manually disabled the toggle...');
    await new Promise(resolve => {
      process.stdin.once('data', () => resolve());
    });
  }

  return toggleFound;
}

async function deleteAllPasskeys(page) {
  console.log('\n🗑️  Step 2: Deleting all passkeys...');

  // Navigate to passkeys page
  await page.goto('https://myaccount.google.com/signinoptions/passkeys', { waitUntil: 'networkidle2' });
  await page.waitForTimeout(3000);
  await screenshot(page, 'passkeys-page-initial');

  let deletedCount = 0;
  let iteration = 0;
  const maxIterations = 20; // Safety limit

  while (iteration < maxIterations) {
    iteration++;

    // Look for delete buttons (X icons or delete buttons)
    const deleteSelectors = [
      'button[aria-label*="Remove"]',
      'button[aria-label*="Delete"]',
      'button[data-tooltip*="Remove"]',
      'button[data-tooltip*="Delete"]',
      '[role="button"][aria-label*="Remove"]',
      'div[data-rid] button',
      'c-wiz button[jsname]'
    ];

    let deleteButton = null;

    for (const selector of deleteSelectors) {
      try {
        const buttons = await page.$$(selector);

        for (const button of buttons) {
          const ariaLabel = await page.evaluate(el => el.getAttribute('aria-label'), button);
          const text = await page.evaluate(el => el.textContent, button);

          if ((ariaLabel && (ariaLabel.toLowerCase().includes('remove') ||
                             ariaLabel.toLowerCase().includes('delete'))) ||
              (text && (text.toLowerCase().includes('remove') ||
                       text.toLowerCase().includes('delete')))) {
            deleteButton = button;
            break;
          }
        }

        if (deleteButton) break;
      } catch (error) {
        continue;
      }
    }

    if (!deleteButton) {
      console.log('✅ No more passkeys found to delete');
      break;
    }

    // Click delete button
    console.log(`🗑️  Deleting passkey ${deletedCount + 1}...`);
    await deleteButton.click();
    await page.waitForTimeout(1500);
    await screenshot(page, `passkey-delete-${deletedCount + 1}-confirm`);

    // Look for confirmation dialog and confirm deletion
    const confirmSelectors = [
      'button[aria-label*="Remove"]',
      'button:contains("Remove")',
      'button:contains("Delete")',
      'button:contains("Confirm")',
      'div[role="dialog"] button'
    ];

    let confirmed = false;

    for (const selector of confirmSelectors) {
      try {
        const confirmButtons = await page.$$(selector);

        for (const button of confirmButtons) {
          const text = await page.evaluate(el => el.textContent, button);

          if (text && (text.toLowerCase().includes('remove') ||
                       text.toLowerCase().includes('delete') ||
                       text.toLowerCase().includes('confirm'))) {
            await button.click();
            confirmed = true;
            console.log('✅ Confirmed deletion');
            await page.waitForTimeout(2000);
            await screenshot(page, `passkey-deleted-${deletedCount + 1}`);
            deletedCount++;
            break;
          }
        }

        if (confirmed) break;
      } catch (error) {
        continue;
      }
    }

    if (!confirmed) {
      console.log('⚠️  Could not find confirmation button - may have auto-confirmed');
      deletedCount++;
      await page.waitForTimeout(2000);
    }

    // Reload page to get fresh list
    await page.reload({ waitUntil: 'networkidle2' });
    await page.waitForTimeout(2000);
  }

  if (iteration >= maxIterations) {
    console.log('⚠️  Reached maximum iterations - there may be more passkeys to delete manually');
  }

  await screenshot(page, 'passkeys-page-final');
  return deletedCount;
}

async function main() {
  console.log('🚀 Google Passkey Disabler Starting...\n');

  const browser = await puppeteer.launch({
    headless: false, // Show browser so you can log in
    defaultViewport: { width: 1280, height: 720 },
    args: ['--start-maximized']
  });

  const page = await browser.newPage();

  try {
    // Navigate to Google login
    console.log('🔐 Step 0: Please log in to your Google account...');
    await page.goto('https://accounts.google.com', { waitUntil: 'networkidle2' });

    // Wait for user to complete login
    console.log('\n⏸️  Press ENTER after you have successfully logged in...');
    await new Promise(resolve => {
      process.stdin.once('data', () => resolve());
    });

    await screenshot(page, 'logged-in');

    // Step 1: Disable passkey requirement
    const toggleDisabled = await disablePasskeyRequirement(page);

    // Step 2: Delete all passkeys
    const deletedCount = await deleteAllPasskeys(page);

    // Final summary
    console.log('\n' + '='.repeat(60));
    console.log('✅ COMPLETED!');
    console.log('='.repeat(60));
    console.log(`📊 Summary:`);
    console.log(`   - "Skip password when possible": ${toggleDisabled ? 'DISABLED' : 'CHECK MANUALLY'}`);
    console.log(`   - Passkeys deleted: ${deletedCount}`);
    console.log(`   - Screenshots saved to: ${screenshotsDir}`);
    console.log('='.repeat(60));

    console.log('\n⏸️  Press ENTER to close browser...');
    await new Promise(resolve => {
      process.stdin.once('data', () => resolve());
    });

  } catch (error) {
    console.error('❌ Error:', error.message);
    await screenshot(page, 'error-state');
    throw error;
  } finally {
    await browser.close();
  }
}

// Run the script
main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
