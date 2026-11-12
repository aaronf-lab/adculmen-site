// Paste each Stripe Payment Link URL between the quotes (dashboard.stripe.com > Payment Links > Copy link).
// Leave a value empty and that button falls back to ordering by email. Nothing else on the site needs editing.
window.STRIPE_LINKS = {
  record: "",               // $0.20 per record, quantity adjustable 1,250-9,999
  record_10k: "",           // $0.15 per record, quantity adjustable 10,000-49,999
  record_50k: "",           // $0.10 per record, quantity adjustable 50,000+
  sub_monthly: "",          // $149 / month
  sub_quarterly: "",        // $399 / 3 months
  sub_annual_region: "",    // $1,490 / year
  sub_annual_statewide: ""  // $3,990 / year
};
