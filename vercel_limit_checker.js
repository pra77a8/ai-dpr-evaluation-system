// Simple script to calculate when Vercel deployment limit will reset
console.log('=== Vercel Deployment Limit Checker ===\n');

// Vercel resets the limit at 00:00 UTC each day
const now = new Date();
const utcReset = new Date(now);
utcReset.setUTCHours(0, 0, 0, 0);
utcReset.setDate(utcReset.getDate() + 1); // Next UTC midnight

// Calculate time until reset
const timeUntilReset = utcReset - now;
const hoursUntilReset = Math.ceil(timeUntilReset / (1000 * 60 * 60));

console.log(`Current time (local): ${now.toLocaleString()}`);
console.log(`Current time (UTC): ${now.toISOString()}`);
console.log(`Next reset time (UTC): ${utcReset.toISOString()}`);
console.log(`\n⏰ Time until deployment limit resets: ~${hoursUntilReset} hours (${Math.floor(timeUntilReset / (1000 * 60 * 60))}h ${Math.floor((timeUntilReset % (1000 * 60 * 60)) / (1000 * 60))}m)`);

// Additional helpful information
console.log('\n=== Helpful Tips ===');
console.log('1. While waiting, you can:');
console.log('   - Test your application locally with "npm run dev"');
console.log('   - Verify your build with "npm run build"');
console.log('   - Test frontend-backend communication locally');
console.log('   - Prepare documentation or marketing materials');
console.log('\n2. When the limit resets:');
console.log('   - Make sure all your recent changes are committed and pushed');
console.log('   - Trigger a deployment from your Vercel dashboard');
console.log('   - Monitor the deployment logs for any issues');

// Calculate approximate reset time in local time
const localReset = new Date(utcReset);
console.log(`\n=== Local Time Information ===`);
console.log(`Reset time in your local timezone: ${localReset.toLocaleString()}`);
console.log(`Reset time in your timezone: ${Intl.DateTimeFormat().resolvedOptions().timeZone}`);