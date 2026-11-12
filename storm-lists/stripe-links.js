// Stripe Payment Links for adculmen.com/storm-lists/order. Seller: Forensic Roofing Sciences LLC (acct_1UVtAlKIQCtKtQQl).
// MODE: TEST (Stripe sandbox, buy.stripe.com/test_...). No real money moves. Swap to the live links once the account is activated.
// Leave a value empty and that button falls back to ordering by email.
window.STRIPE_MODE = "test";
// LIVE links (Forensic Roofing Sciences LLC, acct_1UVtAlKIQCtKtQQl), created Nov 12. Account is PAUSED until the EIN is added,
// so the page stays on the TEST links. To go live: set STRIPE_MODE = "live" (one line) after Stripe shows the account active.
window.STRIPE_LINKS_LIVE = {
  record: "https://buy.stripe.com/7sY28s2Ae9B94MsacS5EY04",               // $0.20 per record, quantity 1,250-9,999
  record_10k: "https://buy.stripe.com/3cI28scaO14D1Agfxc5EY05",           // $0.15 per record, quantity 10,000-49,999
  record_50k: "https://buy.stripe.com/8x28wQfn08x56UAcl05EY06",           // $0.10 per record, quantity 50,000+
  sub_monthly: "https://buy.stripe.com/aFa6oI8YCaFd3Iocl05EY03",          // $149 / month
  sub_quarterly: "https://buy.stripe.com/bJe28s3EiaFdfr6fxc5EY02",        // $399 / 3 months
  sub_annual_region: "https://buy.stripe.com/fZu3cw1wacNl0wc5WC5EY01",    // $1,490 / year
  sub_annual_statewide: "https://buy.stripe.com/7sY8wQb6KaFd5QwacS5EY00"  // $3,990 / year
};
window.STRIPE_LINKS_TEST = {
  record: "https://buy.stripe.com/test_7sY8wQb6KaFd5QwacS5EY00",               // $0.20 per record, quantity 1,250-9,999
  record_10k: "https://buy.stripe.com/test_fZu3cw1wacNl0wc5WC5EY01",           // $0.15 per record, quantity 10,000-49,999
  record_50k: "https://buy.stripe.com/test_bJe28s3EiaFdfr6fxc5EY02",           // $0.10 per record, quantity 50,000+
  sub_monthly: "https://buy.stripe.com/test_aFa6oI8YCaFd3Iocl05EY03",          // $149 / month
  sub_quarterly: "https://buy.stripe.com/test_7sY28s2Ae9B94MsacS5EY04",        // $399 / 3 months
  sub_annual_region: "https://buy.stripe.com/test_3cI28scaO14D1Agfxc5EY05",    // $1,490 / year
  sub_annual_statewide: "https://buy.stripe.com/test_8x28wQfn08x56UAcl05EY06"  // $3,990 / year
};
window.STRIPE_LINKS = window.STRIPE_MODE === "live" ? window.STRIPE_LINKS_LIVE : window.STRIPE_LINKS_TEST;

// While MODE is "test", show a notice on the order page so no buyer mistakes a sandbox checkout for a real order.
if (window.STRIPE_MODE === "test") document.addEventListener("DOMContentLoaded", function () {
  var m = document.querySelector("main") || document.body, d = document.createElement("div");
  d.setAttribute("role", "note");
  d.style.cssText = "border:1px solid #c8a45a;background:#2a2416;color:#f3e6c4;padding:10px 14px;margin:12px auto;max-width:960px;font-size:14px;line-height:1.45";
  d.textContent = "Card checkout is in TEST mode this week: no card is charged and no list is delivered. To order now, email aaron@forensicroofingsciences.com or call (651) 349-4377 and we will invoice you.";
  m.insertBefore(d, m.firstChild);
});
