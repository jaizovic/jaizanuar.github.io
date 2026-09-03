(function () {
  'use strict';

  var siteCode = 'jaizanuar';
  var counterBase = 'https://' + siteCode + '.goatcounter.com/counter/';
  var articleLimit = 20;
  var articles = [
    ["Industrial Security Assumed Attackers Needed Rare Expertise. AI Is Changing That Assumption.", "2026-09-03", "/articles/industrial-security-assumed-attackers-needed-rare-expertise-ai-is-changing-that-assumption.html"],
    ["The SOC Detected the Attack. The Organisation Still Lost the Domain.", "2026-09-02", "/articles/the-soc-detected-the-attack-the-organisation-still-lost-the-domain.html"],
    ["Too Experienced to Hire, Too Young to Retire: The Cybersecurity Career Trap for Gen X", "2026-09-01", "/articles/too-experienced-to-hire-too-young-to-retire-the-cybersecurity-career-trap-for-gen-x.html"],
    ["When an AI Security Test Becomes a Real Cyber Incident, Who Owns the Breach?", "2026-08-30", "/articles/when-an-ai-security-test-becomes-a-real-cyber-incident-who-owns-the-breach.html"],
    ["Your Vendor Passed the Security Assessment. The Breach Still Came Through Them.", "2026-08-29", "/articles/your-vendor-passed-the-security-assessment-the-breach-still-came-through-them.html"],
    ["Your Employer Manages Your Increment. You Manage Your Career.", "2026-08-25", "/articles/your-employer-manages-your-increment-you-manage-your-career.html"],
    ["The Tools We Trust To Secure The Supply Chain Can Become The Supply Chain Risk", "2026-08-23", "/articles/the-tools-we-trust-to-secure-the-supply-chain-can-become-the-supply-chain-risk.html"],
    ["Critical Infrastructure Was Designed To Be Reliable. Now It Must Be Designed To Survive AI-Assisted Attacks.", "2026-08-22", "/articles/critical-infrastructure-was-designed-to-be-reliable-now-it-must-be-designed-to-survive-ai-assisted-attacks.html"],
    ["Tomorrow’s Technology Cannot Be Protected With Yesterday’s Security Architecture", "2026-08-19", "/articles/tomorrows-technology-cannot-be-protected-with-yesterdays-security-architecture.html"],
    ["The Most Dangerous Attacker Is The One Who Does Not Need To Rush", "2026-08-16", "/articles/the-most-dangerous-attacker-is-the-one-who-does-not-need-to-rush.html"],
    ["AI Is Not Creating New Attack Techniques. It Is Removing The Time Between Them.", "2026-08-15", "/articles/ai-is-not-creating-new-attack-techniques-it-is-removing-the-time-between-them.html"],
    ["The Security Tools We Forgot to Retire", "2026-08-13", "/articles/the-security-tools-we-forgot-to-retire.html"],
    ["More Accounts, Less Trust: The Slow Decline of Social Media", "2026-08-12", "/articles/more-accounts-less-trust-the-slow-decline-of-social-media.html"],
    ["Cybersecurity Is a Choice We Make Every Day", "2026-08-10", "/articles/cybersecurity-is-a-choice-we-make-every-day.html"],
    ["The Most Dangerous Software May Be the Software You Never Use", "2026-08-07", "/articles/the-most-dangerous-software-may-be-the-software-you-never-use.html"],
    ["AI Agents Need Security Boundaries, Not Just Safety Guardrails", "2026-08-07", "/articles/ai-agents-need-security-boundaries-not-just-safety-guardrails.html"],
    ["Technical Skills Get You Hired. Judgement Gets You Promoted.", "2026-08-06", "/articles/technical-skills-get-you-hired-judgement-gets-you-promoted.html"],
    ["The Best Cybersecurity Leaders Build More Leaders, Not More Followers", "2026-08-05", "/articles/the-best-cybersecurity-leaders-build-more-leaders-not-more-followers.html"],
    ["Good Security Architecture Assumes Every Control Will Eventually Fail", "2026-08-04", "/articles/good-security-architecture-assumes-every-control-will-eventually-fail.html"],
    ["Shadow IT Is Not the Problem. Invisible Risk Is.", "2026-08-03", "/articles/shadow-it-is-not-the-problem-invisible-risk-is.html"],
    ["Risk Acceptance Is Not Risk Transfer", "2026-08-02", "/articles/risk-acceptance-is-not-risk-transfer.html"],
    ["DSPM, DLP and CASB: Complementary Controls or Expensive Overlap?", "2026-07-31", "/articles/dspm-dlp-and-casb-complementary-controls-or-expensive-overlap.html"],
    ["Don't Chase Cybersecurity Certifications. Chase A Career Strategy.", "2026-07-29", "/articles/dont-chase-cybersecurity-certifications-chase-a-career-strategy.html"],
    ["The Next CISO Will Lead Humans, Machines and AI Agents; Not Just People", "2026-07-27", "/articles/the-next-ciso-will-lead-humans-machines-and-ai-agents-not-just-people.html"],
    ["SIEM Migration Checklist: How to Avoid Detection Gaps", "2026-07-25", "/articles/siem-migration-checklist-how-to-avoid-detection-gaps.html"],
    ["The Next Insider Threat May Not Be Human. It May Be an AI Agent.", "2026-07-25", "/articles/the-next-insider-threat-may-not-be-human-it-may-be-an-ai-agent.html"],
    ["Good Security Architecture Begins With Better Questions", "2026-07-24", "/articles/good-security-architecture-begins-with-better-questions.html"],
    ["Security Architecture Is Where Trust, Controls and Resilience Come Together", "2026-07-23", "/articles/security-architecture-is-where-trust-controls-and-resilience-come-together.html"],
    ["A SIEM Migration Is Not Just a Technology Refresh. It Is a Security Risk Event.", "2026-07-23", "/articles/a-siem-migration-is-not-just-a-technology-refresh-it-is-a-security-risk-event.html"],
    ["Security Architecture Protects The Business; Security Controls Protect The Technology", "2026-07-22", "/articles/security-architecture-protects-the-business-security-controls-protect-the-technology.html"],
    ["The Best Security Architects Know How Systems Break", "2026-07-21", "/articles/the-best-security-architects-know-how-systems-break.html"],
    ["The Next Generation Cyber Community Must Learn More Than How to Hack", "2026-07-20", "/articles/the-next-generation-cyber-community-must-learn-more-than-how-to-hack.html"],
    ["Cybersecurity Is Becoming A Trust Engineering Discipline", "2026-07-19", "/articles/cybersecurity-is-becoming-a-trust-engineering-discipline.html"],
    ["Attackers Are Becoming AI-Native. Deception Must Become AI-Native Too.", "2026-07-18", "/articles/attackers-are-becoming-ai-native-deception-must-become-ai-native-too.html"],
    ["The New Security Perimeter Is No Longer The Network. It Is Identity.", "2026-07-17", "/articles/the-new-security-perimeter-is-no-longer-the-network-it-is-identity.html"],
    ["The Biggest AI Deployment In Your Organisation May Already Be Happening Without You", "2026-07-17", "/articles/the-biggest-ai-deployment-in-your-organisation-may-already-be-happening-without-you.html"],
    ["Employees Are Adopting AI Faster Than Organisations Can Govern It", "2026-07-17", "/articles/employees-are-adopting-ai-faster-than-organisations-can-govern-it.html"],
    ["Most Architecture Diagrams Show Connectivity. Few Show Trust and Controls.", "2026-07-16", "/articles/most-architecture-diagrams-show-connectivity-few-show-trust-and-controls.html"],
    ["Enable Business Safely, Not Block Business Safely", "2026-07-15", "/articles/enable-business-safely-not-block-business-safely.html"],
    ["Cybersecurity Best Practice Is a Baseline, Not a Blueprint", "2026-07-14", "/articles/cybersecurity-best-practice-baseline-not-blueprint.html"],
    ["The Real Risk of AI Coding Agents Is Not Intelligence. It Is Permission.", "2026-07-10", "/articles/the-real-risk-of-ai-coding-agents-is-permission.html"],
    ["Not All Personal Data Can Be Anonymised; But All Personal Data Must Be Governed", "2026-07-10", "/articles/not-all-personal-data-can-be-anonymised.html"],
    ["Convenience Is an Attack Surface", "2026-07-09", "/articles/convenience-is-an-attack-surface.html"],
    ["When Active Directory Works, But Is Not Resilient", "2026-07-07", "/articles/when-active-directory-works-but-is-not-resilient.html"],
    ["Zero Trust Is Not About Trust. It Is About Reducing the Cost of Being Wrong.", "2026-07-04", "/articles/zero-trust-reducing-cost-of-being-wrong.html"],
    ["The Most Dangerous Incidents Start as Normal Days", "2026-06-29", "/articles/the-most-dangerous-incidents-start-as-normal-days.html"],
    ["Three Reasons You Haven’t Been Hacked... Yet. Only One Is Good News.", "2026-06-25", "/articles/three-reasons-you-havent-been-hacked.html"],
    ["If the Cybersecurity Industry Profits from Cyberattacks, Why Do We Rely on Its Vendors to Tell Us How Secure We Are?", "2026-06-19", "/articles/cybersecurity-industry-profits.html"],
    ["Three Types of Cybersecurity Confidence. Which One Does Your Organisation Have?", "2026-06-16", "/articles/three-types-of-cybersecurity-confidence.html"],
    ["Cybersecurity Doesn't Fail Because We Don't Know Enough. It Fails Because We Become Too Certain About What We Think We Know.", "2026-06-07", "/articles/cybersecurity-doesnt-fail-because-we-dont-know-enough.html"],
    ["You Cannot Report a Data Breach You Cannot See", "2025-09-19", "/articles/you-cannot-report-a-data-breach-you-cannot-see.html"],
    ["The Best Cybersecurity Candidate May Not Have the Certification You Asked For", "2025-08-31", "/articles/the-best-cybersecurity-candidate-may-not-have-the-certification-you-asked-for.html"],
    ["When Security Tools Become the Noise", "2025-04-12", "/articles/when-security-tools-become-the-noise.html"],
    ["Behind Every Line of Code: The Human Element of Cybersecurity", "2025-03-19", "/articles/behind-every-line-of-code-human-element-cybersecurity.html"],
    ["A CISO Cannot Lead Every Operating Model the Same Way", "2025-02-18", "/articles/a-ciso-cannot-lead-every-operating-model-the-same-way.html"],
    ["Real Data Breach vs Honeypot Data Breach", "2024-05-23", "/articles/real-data-breach-vs-honeypot-data-breach.html"]
  ];

  function dateString(date) {
    var year = date.getFullYear();
    var month = String(date.getMonth() + 1).padStart(2, '0');
    var day = String(date.getDate()).padStart(2, '0');
    return year + '-' + month + '-' + day;
  }

  function counterUrl(path, start, end) {
    var url = counterBase + encodeURIComponent(path) + '.json';
    var params = new URLSearchParams();
    if (start) params.set('start', start);
    if (end) params.set('end', end);
    return url + (params.toString() ? '?' + params.toString() : '');
  }

  async function getCount(path, start, end) {
    var controller = new AbortController();
    var timeout = window.setTimeout(function () { controller.abort(); }, 8000);
    var response;
    try {
      response = await fetch(counterUrl(path, start, end), { mode: 'cors', signal: controller.signal });
    } finally {
      window.clearTimeout(timeout);
    }
    if (!response.ok) throw new Error('Analytics are not active yet');
    var data = await response.json();
    return Number(String(data.count || '0').replace(/[^0-9]/g, '')) || 0;
  }

  function formatNumber(number) {
    return new Intl.NumberFormat('en-MY').format(number);
  }

  function formatDate(value) {
    return new Intl.DateTimeFormat('en-MY', { day: 'numeric', month: 'short', year: 'numeric' }).format(new Date(value + 'T00:00:00'));
  }

  function setLoading(isLoading) {
    var button = document.getElementById('refreshButton');
    button.disabled = isLoading;
    button.textContent = isLoading ? 'Refreshing…' : 'Refresh';
  }

  function renderRows(results) {
    var rows = document.getElementById('articleRows');
    var maximum = Math.max.apply(null, results.map(function (item) { return item.count; }).concat([1]));
    rows.replaceChildren();

    results.forEach(function (item) {
      var row = document.createElement('tr');
      var titleCell = document.createElement('td');
      var link = document.createElement('a');
      var bar = document.createElement('span');
      var dateCell = document.createElement('td');
      var countCell = document.createElement('td');

      link.href = '..' + item.path;
      link.textContent = item.title;
      bar.className = 'visit-bar';
      bar.style.setProperty('--bar-width', ((item.count / maximum) * 100).toFixed(1) + '%');
      titleCell.append(link, bar);
      dateCell.textContent = formatDate(item.date);
      dateCell.className = 'date-cell';
      countCell.textContent = formatNumber(item.count);
      countCell.className = 'number-cell count-value';
      row.append(titleCell, dateCell, countCell);
      rows.appendChild(row);
    });
  }

  function countryFlag(code) {
    return String.fromCodePoint.apply(null, code.toUpperCase().split('').map(function (letter) {
      return 127397 + letter.charCodeAt(0);
    }));
  }

  function renderReaderCountries(countries) {
    var list = document.getElementById('countryList');
    list.replaceChildren();

    if (!countries.length) {
      var empty = document.createElement('li');
      empty.className = 'country-loading';
      empty.textContent = 'Reader locations will appear after the country feed is updated.';
      list.appendChild(empty);
      return;
    }

    countries.slice(0, 25).forEach(function (country) {
      var item = document.createElement('li');
      var flag = document.createElement('span');
      var name = document.createElement('span');

      flag.className = 'country-flag';
      flag.textContent = countryFlag(country.code);
      flag.setAttribute('aria-hidden', 'true');
      name.className = 'country-name';
      name.textContent = country.name;
      item.append(flag, name);
      list.appendChild(item);
    });
  }

  async function loadReaderCountries() {
    try {
      var response = await fetch('../data/reader-countries.json', { cache: 'no-cache' });
      if (!response.ok) throw new Error('Country feed is not available');
      var data = await response.json();
      var countries = Array.isArray(data.countries) ? data.countries.filter(function (country) {
        return country && /^[A-Z]{2}$/.test(country.code) && typeof country.name === 'string';
      }) : [];
      renderReaderCountries(countries);
    } catch (error) {
      renderReaderCountries([]);
    }
  }

  async function loadDashboard() {
    setLoading(true);
    document.getElementById('setupPanel').hidden = true;
    document.getElementById('statusText').textContent = 'Loading live data';
    document.getElementById('liveStatus').classList.remove('status-error');

    var today = new Date();
    var monthStart = new Date(today);
    monthStart.setDate(today.getDate() - 29);
    var todayText = dateString(today);

    try {
      var summaryPromise = Promise.all([
        getCount('TOTAL'),
        getCount('TOTAL', todayText, todayText),
        getCount('TOTAL', dateString(monthStart), todayText)
      ]);
      var articlePromise = Promise.all(articles.map(async function (article) {
        var count;
        try { count = await getCount(article[2]); } catch (error) { count = 0; }
        return { title: article[0], date: article[1], path: article[2], count: count };
      }));

      var data = await Promise.all([summaryPromise, articlePromise]);
      var summary = data[0];
      var articleResults = data[1].sort(function (a, b) { return b.count - a.count || b.date.localeCompare(a.date); });
      var topArticleResults = articleResults.slice(0, articleLimit);
      var topArticle = articleResults[0];

      document.getElementById('totalVisits').textContent = formatNumber(summary[0]);
      document.getElementById('todayVisits').textContent = formatNumber(summary[1]);
      document.getElementById('monthVisits').textContent = formatNumber(summary[2]);
      document.getElementById('topArticleVisits').textContent = formatNumber(topArticle.count);
      document.getElementById('topArticleTitle').textContent = topArticle.title;
      document.getElementById('todayLabel').textContent = new Intl.DateTimeFormat('en-MY', { day: 'numeric', month: 'long' }).format(today);
      renderRows(topArticleResults);
      document.getElementById('articleCount').textContent = 'Top ' + topArticleResults.length + ' articles';
      document.getElementById('statusText').textContent = 'Live data';
    } catch (error) {
      document.getElementById('totalVisits').textContent = '—';
      document.getElementById('todayVisits').textContent = '—';
      document.getElementById('monthVisits').textContent = '—';
      document.getElementById('topArticleVisits').textContent = '—';
      document.getElementById('topArticleTitle').textContent = 'Analytics setup required';
      document.getElementById('articleRows').innerHTML = '<tr><td colspan="3" class="loading-cell">Visitor data will appear here after analytics is activated.</td></tr>';
      document.getElementById('setupPanel').hidden = false;
      document.getElementById('statusText').textContent = 'Setup required';
      document.getElementById('liveStatus').classList.add('status-error');
    } finally {
      setLoading(false);
    }
  }

  document.getElementById('articleCount').textContent = 'Top ' + Math.min(articleLimit, articles.length) + ' articles';
  document.getElementById('refreshButton').addEventListener('click', function () {
    loadReaderCountries();
    loadDashboard();
  });
  loadReaderCountries();
  loadDashboard();
}());
