'use strict';

const menuButton = document.querySelector('.menu-button');
const navigation = document.querySelector('#navigation');
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('is-open', open);
});
navigation.addEventListener('click', (event) => {
  if (event.target.closest('a')) {
    menuButton.setAttribute('aria-expanded', 'false');
    navigation.classList.remove('is-open');
  }
});

const examples = {
  live: {label: '01', title: 'A prompt is useful only if it arrives in time.', description: 'Follow a defined interaction event through delivery of a visible, usable prompt. Review timeliness and failed delivery separately.', path: ['Interaction event', 'Processing', 'Usable prompt'], measure: 'Median and p95 delivery time, timely-delivery rate, failed deliveries', review: 'Comparable scenarios, relevant release changes, evidence gaps', prevent: 'Repeatable checks and documented decisions for threshold breaches'},
  document: {label: '02', title: 'A completed job should mean a usable result.', description: 'Follow a representative upload through processing and result delivery. Compare like workloads and keep failures visible.', path: ['Document upload', 'Analysis job', 'Result delivery'], measure: 'Processing-time distributions, completion, retries, attributable compute cost', review: 'Workload size, comparable environments, release and dependency changes', prevent: 'Regression checks, completion criteria, mitigation and exception records'},
  voice: {label: '03', title: 'Make the first exchange a measurable journey.', description: 'Follow an eligible scheduled call through setup and a defined first exchange. Separate non-answer, technical failures, and unresolved outcomes.', path: ['Scheduled initiation', 'Call setup', 'First exchange'], measure: 'Initiation delay, setup success, response time, incomplete interactions', review: 'Comparable scenarios, provider outcomes, release changes, known limitations', prevent: 'Targeted pre-release checks, escalation, documented decisions and follow-up'}
};
const tabs = [...document.querySelectorAll('[role="tab"]')];
function activateTab(tab) {
  const example = examples[tab.dataset.case];
  tabs.forEach((item) => {
    item.setAttribute('aria-selected', String(item === tab));
    item.tabIndex = item === tab ? 0 : -1;
  });
  document.querySelector('#use-case-panel').setAttribute('aria-labelledby', tab.id);
  document.querySelector('.case-label').textContent = `ILLUSTRATIVE WORKFLOW / ${example.label}`;
  for (const field of ['title', 'description', 'measure', 'review', 'prevent']) {
    document.querySelector(`#case-${field}`).textContent = example[field];
  }
  document.querySelectorAll('#case-path span').forEach((item, index) => { item.textContent = example.path[index]; });
}
tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => activateTab(tab));
  tab.addEventListener('keydown', (event) => {
    let next;
    if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
    if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = tabs.length - 1;
    if (next !== undefined) { event.preventDefault(); activateTab(tabs[next]); tabs[next].focus(); }
  });
});

const scenario = document.querySelector('#scenario');
const evidenceCheck = document.querySelector('#evidence-check');
function updateIllustration() {
  let title, description, code, color;
  const value = scenario.value;
  const candidate = document.querySelector('#candidate-value');
  if (value === 'incomplete') {
    candidate.textContent = '—';
    title = 'Collect comparable evidence';
    description = 'The candidate measurement is incomplete. A recorded owner does not replace missing benchmark evidence.';
    code = 'MEASUREMENT REQUIRED'; color = '#efaa8b';
  } else if (value === 'regression') {
    candidate.innerHTML = '1040<small> ms</small>';
    title = 'Mitigate & validate again';
    description = 'The synthetic candidate is 30% above baseline. Recording the review does not clear a threshold breach; mitigation and further validation are needed.';
    code = 'THRESHOLD EXCEEDED'; color = '#efaa8b';
  } else {
    candidate.innerHTML = '820<small> ms</small>';
    title = evidenceCheck.checked ? 'Ready for the next review' : 'Complete the evidence record';
    description = evidenceCheck.checked ? 'The synthetic candidate is 2.5% above baseline and the example record is complete. Other release checks and an authorized decision are still required.' : 'Performance is within the example threshold. A named review owner and supporting evidence are still needed.';
    code = evidenceCheck.checked ? 'EXAMPLE CHECKS COMPLETE' : 'EVIDENCE REQUIRED';
    color = evidenceCheck.checked ? '#c8d4b9' : '#efaa8b';
  }
  document.querySelector('#result-title').textContent = title;
  document.querySelector('#result-description').textContent = description;
  document.querySelector('#result-code').textContent = code;
  document.querySelector('#result-indicator').style.color = color;
}
scenario.addEventListener('change', updateIllustration);
evidenceCheck.addEventListener('change', updateIllustration);
updateIllustration();
