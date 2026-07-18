(function () {
  'use strict';

  var siteCode = 'jaizanuar';
  var counterBase = 'https://' + siteCode + '.goatcounter.com/counter/';
  var articles = [
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
    ["When Security Tools Become the Noise", "2025-04-12", "/articles/when-security-tools-become-the-noise.html"],
    ["Behind Every Line of Code: The Human Element of Cybersecurity", "2025-03-19", "/articles/behind-every-line-of-code-human-element-cybersecurity.html"],
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
      var topArticle = articleResults[0];

      document.getElementById('totalVisits').textContent = formatNumber(summary[0]);
      document.getElementById('todayVisits').textContent = formatNumber(summary[1]);
      document.getElementById('monthVisits').textContent = formatNumber(summary[2]);
      document.getElementById('topArticleVisits').textContent = formatNumber(topArticle.count);
      document.getElementById('topArticleTitle').textContent = topArticle.title;
      document.getElementById('todayLabel').textContent = new Intl.DateTimeFormat('en-MY', { day: 'numeric', month: 'long' }).format(today);
      renderRows(articleResults);
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

  document.getElementById('articleCount').textContent = articles.length + ' articles';
  document.getElementById('refreshButton').addEventListener('click', loadDashboard);
  loadDashboard();
}());
