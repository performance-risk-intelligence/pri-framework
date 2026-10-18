'use strict';

/**
 * PRI sandbox: self-contained, synthetic teaching model.
 * No data persistence, network calls, validated predictive model, or production authority.
 */
(() => {
  const $ = (id) => document.getElementById(id);
  const values = {
    coaching: {name:'Real-time AI coaching prompt',unit:'ms',p95:900,success:99.5,retry:0.8,cost:0.05,incidents:[
      {title:'Delayed prompts after a dependency update',signal:'latency',severity:'high',investigation:'Cause suspected',prevention:''},
      {title:'Retry amplification across an integration',signal:'retry',severity:'medium',investigation:'Reviewed',prevention:'Retry-limit test proposed'}]},
    document: {name:'Document-to-analysis job',unit:'sec',p95:65,success:99.1,retry:1.4,cost:0.21,incidents:[
      {title:'Analysis slowdown after a model update',signal:'latency',severity:'medium',investigation:'Under review',prevention:''},
      {title:'Timeout during a document batch run',signal:'success',severity:'high',investigation:'Cause suspected',prevention:''}]},
    voice: {name:'Scheduled voice first exchange',unit:'ms',p95:2050,success:98.9,retry:1.2,cost:0.09,incidents:[
      {title:'Call setup timeout during a provider change',signal:'success',severity:'high',investigation:'Attribution unresolved',prevention:''},
      {title:'First response latency regression',signal:'latency',severity:'medium',investigation:'Reviewed',prevention:'Synthetic first-turn test proposed'}]}
  };
  const presets = {
    steady:{p95:1.04,successDrop:0.1,retryIncrease:0.2,cost:1.03,coverage:96,complexity:1},
    regression:{p95:1.45,successDrop:3.1,retryIncrease:2.9,cost:1.34,coverage:72,complexity:4},
    missing:{p95:null,successDrop:null,retryIncrease:null,cost:null,coverage:35,complexity:3}
  };
  let incidents=[],audit=[],serial=0;
  const set=(id,value)=>{$(id).textContent=String(value)};
  const n=(id,min=0,max=1e10)=>{
    const el=$(id);
    if(!el||!el.value.trim()||!el.validity.valid)return null;
    const v=Number(el.value);
    return Number.isFinite(v)&&v>=min&&v<=max?v:null;
  };
  const diff=(candidate,baseline)=>candidate===null||baseline===0?null:100*(candidate/baseline-1);
  const signed=(v,unit,digits=1)=>v===null?'Not measured':(v>0?'+':'')+v.toFixed(digits)+unit;
  const money=(v)=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(v);
  const integer=(v)=>new Intl.NumberFormat('en-US',{maximumFractionDigits:0}).format(v);
  const w=()=>values[$('workflow').value];
  const snapshot=()=>({p95:n('p95',.01),success:n('success',0,100),retry:n('retry',0,100),cost:n('cost'),coverage:n('test-coverage',0,100),complexity:Number($('complexity').value)});
  const msg=(s)=>set('app-status',s);

  function resetCandidate(withIncidents=true){
    const b=w(),p=presets[$('scenario').value];
    const inits={p95:p.p95===null?'':(b.p95*p.p95).toFixed(b.unit==='sec'?1:0),
      success:p.successDrop===null?'':(b.success-p.successDrop).toFixed(1),
      retry:p.retryIncrease===null?'':(b.retry+p.retryIncrease).toFixed(1),
      cost:p.cost===null?'':(b.cost*p.cost).toFixed(3),
      'test-coverage':p.coverage,complexity:p.complexity};
    for(const [key,value] of Object.entries(inits))$(key).value=value;
    if(withIncidents){incidents=b.incidents.map((entry,index)=>({...entry,id:index+1}));serial=incidents.length;}
    audit=[];
    $('decision-form').reset();
    render();
  }
  function scoreRisk(x,b){
    const dp=diff(x.p95,b.p95);
    const successDrop=x.success===null?null:b.success-x.success;
    const retryRise=x.retry===null?null:x.retry-b.retry;
    const highOpen=incidents.filter((v)=>v.severity==='high'&&!v.prevention).length;
    const factors=[
      {title:'p95 latency regression',points:dp===null?null:dp>25?35:dp>10?22:dp>5?10:2,detail:dp===null?'Candidate measurement missing':signed(dp,'%')+' from baseline'},
      {title:'Completion degradation',points:successDrop===null?null:successDrop>3?25:successDrop>1?14:successDrop>.2?6:0,detail:successDrop===null?'Completion rate missing':successDrop.toFixed(1)+' percentage-point drop'},
      {title:'Retry amplification',points:retryRise===null?null:retryRise>2?15:retryRise>.5?8:0,detail:retryRise===null?'Retry rate missing':signed(retryRise,' percentage points')},
      {title:'Change complexity',points:x.complexity*4,detail:'Illustrative level '+x.complexity+' of 5'},
      {title:'High-severity incidents without a linked action',points:Math.min(18,highOpen*6),detail:highOpen+' unlinked record(s)'},
      {title:'Pre-release checks not completed',points:x.coverage===null?null:x.coverage<80?12:x.coverage<95?5:0,detail:x.coverage===null?'Coverage missing':x.coverage+'% performed'}
    ];
    const missing=[x.p95,x.success,x.retry,x.coverage].some(v=>v===null);
    const score=missing?null:Math.min(100,factors.reduce((total,f)=>total+(f.points||0),0));
    let tier='Incomplete evidence',gate='HOLD: collect comparable evidence',detail='A documented exception is not a substitute for missing measurement evidence.';
    if(score!==null){
      if(score>=60){tier='High risk';gate='BLOCK: mitigation and revalidation required';detail='Investigate the regression, mitigate, and repeat controlled measurements before authorization.'}
      else if(score>=30){tier='Elevated risk';gate='HOLD: enhanced validation required';detail='Review risk drivers, open investigations, and mitigation evidence.'}
      else{tier='Lower risk';gate='REVIEW: example thresholds not exceeded';detail='Other release checks and an authorized human decision remain necessary.'}
    }
    return{factors,score,missing,tier,gate,detail,dp,successDrop,retryRise};
  }
  function renderIncidents(){
    const body=$('incident-table');body.replaceChildren();
    for(const rec of incidents){
      const tr=document.createElement('tr');
      const td1=document.createElement('td');td1.textContent=rec.title;
      const meta=document.createElement('small');meta.className='row-meta';meta.textContent=rec.signal;td1.appendChild(meta);
      const td2=document.createElement('td');td2.textContent=rec.severity;td2.className='severity-'+rec.severity;
      const td3=document.createElement('td');td3.textContent=rec.investigation;
      const td4=document.createElement('td');td4.textContent=rec.prevention||'Not linked';
      if(!rec.prevention){
        td4.appendChild(document.createElement('br'));
        const btn=document.createElement('button');btn.type='button';btn.className='inline-action';btn.textContent='Propose control';
        btn.addEventListener('click',()=>{rec.prevention='Regression test proposed';rec.investigation='Control pending validation';render();msg('A synthetic prevention link was recorded. No implementation is claimed.')});
        td4.appendChild(btn);
      }
      tr.append(td1,td2,td3,td4);body.appendChild(tr);
    }
    set('incident-count',incidents.length+' records');
  }
  function renderAudit(){
    const list=$('audit-list');list.replaceChildren();
    if(!audit.length){const p=document.createElement('p');p.className='muted';p.textContent='No review decisions recorded yet.';list.appendChild(p);}
    else for(const entry of audit.slice().reverse()){
      const item=document.createElement('article');item.className='audit-item';
      const title=document.createElement('strong');title.textContent=entry.choice+' · '+entry.owner;
      const para=document.createElement('p');para.textContent=entry.rationale;
      const time=document.createElement('small');time.textContent=entry.time+' · '+entry.tier+' · hypothetical decision only';
      item.append(title,para,time);list.appendChild(item);
    }
    set('out-decisions',audit.length);
  }
  function renderImpact(){
    const candidate=snapshot();
    const inputs={volume:n('impact-volume'),marginal:n('impact-retry-cost'),
      target:n('impact-target-retry',0,100),hourly:n('impact-hourly'),
      hoursBefore:n('impact-hours-before'),hoursAfter:n('impact-hours-after')};
    const invalid=Object.values(inputs).some(v=>v===null)||candidate.retry===null;
    let retries=0,compute=0,engineering=0,total=0;
    if(!invalid){
      const reduction=Math.max(0,candidate.retry-inputs.target)/100;
      retries=inputs.volume*reduction;
      compute=retries*inputs.marginal;
      engineering=Math.max(0,inputs.hoursBefore-inputs.hoursAfter)*inputs.hourly;
      total=compute+engineering;
    }
    set('impact-retries',invalid?'Missing inputs':integer(retries));
    set('impact-compute',invalid?'N/A':money(compute));
    set('impact-engineering',invalid?'N/A':money(engineering));
    set('impact-total',invalid?'N/A':money(total));
    set('impact-annual',invalid?'N/A':money(total*12));
    set('impact-calculation',invalid?'Enter a valid candidate retry rate and impact assumptions.':
      integer(inputs.volume)+' attempts × '+Math.max(0,candidate.retry-inputs.target).toFixed(1)+' percentage-point fewer retries × $'+inputs.marginal.toFixed(2)+' per retry + '+
      Math.max(0,inputs.hoursBefore-inputs.hoursAfter).toFixed(0)+' recovered engineer-hours × $'+inputs.hourly.toFixed(0)+'/hour.');
  }
  function render(){
    const b=w(),x=snapshot(),r=scoreRisk(x,b);
    set('metric-label','p95 journey time ('+b.unit+')');
    set('candidate-p95-label','p95 time ('+b.unit+')');
    set('base-p95',b.p95+' '+b.unit);
    set('base-success',b.success.toFixed(1)+'%');
    set('base-retry',b.retry.toFixed(1)+'%');
    set('base-cost','$'+b.cost.toFixed(3));
    set('base-bar-text',b.p95+' '+b.unit);
    set('candidate-bar-text',x.p95===null?'Missing':x.p95.toFixed(b.unit==='sec'?1:0)+' '+b.unit);
    const max=Math.max(b.p95,x.p95||0);
    $('base-bar').style.width=(100*b.p95/max)+'%';
    $('candidate-bar').style.width=(x.p95===null?0:100*x.p95/max)+'%';
    $('candidate-bar').classList.toggle('regressed',r.dp!==null&&r.dp>10);
    set('risk-score',r.score===null?'N/A':r.score);
    set('risk-tier',r.tier);set('risk-summary',r.missing?'Required measurement evidence is incomplete.':r.tier==='High risk'?'Multiple synthetic signals warrant mitigation.':r.tier==='Elevated risk'?'Some synthetic signals require additional validation.':'No major example threshold is breached.');
    $('risk-score').className='risk-score '+(r.missing?'incomplete':r.score>=60?'high':r.score>=30?'elevated':'low');
    $('gate').className='gate '+(r.missing||r.score>=60?'gate-hold':r.score>=30?'gate-review':'gate-low');
    set('gate-title',r.gate);set('gate-detail',r.detail);
    const factors=$('score-factors');factors.replaceChildren();
    for(const f of r.factors){const d=document.createElement('div');d.className='factor';
      const name=document.createElement('span');name.textContent=f.title;
      const pts=document.createElement('strong');pts.textContent=f.points===null?'N/A':'+'+f.points;
      const detail=document.createElement('small');detail.textContent=f.detail;
      d.append(name,pts,detail);factors.appendChild(d);}
    renderIncidents();renderAudit();
    const selected=[...document.querySelectorAll('.control-input')].filter(x=>x.checked).length;
    set('control-coverage',selected+' / 4');$('coverage-bar').style.width=(selected*25)+'%';
    set('out-p95',signed(r.dp,'%'));
    set('out-success',signed(x.success===null?null:x.success-b.success,' pp'));
    set('out-retry',signed(x.retry===null?null:x.retry-b.retry,' pp'));
    set('out-cost',signed(diff(x.cost,b.cost),'%'));
    set('out-prevention',incidents.filter(x=>x.prevention).length+' / '+incidents.length);
    renderImpact();
  }
  function resetImpact(){
    const defs={'impact-volume':500000,'impact-retry-cost':0.08,'impact-target-retry':1.2,'impact-hourly':125,'impact-hours-before':80,'impact-hours-after':45};
    for(const [id,value] of Object.entries(defs))$(id).value=value;renderImpact();
  }
  $('workflow').addEventListener('change',()=>{
    $('scenario').value='regression';
    document.querySelectorAll('.control-input').forEach(x=>x.checked=false);
    resetCandidate(true);msg('Loaded a different synthetic workflow, baseline, and incident history.');
  });
  $('scenario').addEventListener('change',()=>{resetCandidate(false);msg('Loaded a synthetic candidate scenario. Existing incident context remains illustrative.')});
  for(const id of ['p95','success','retry','cost','test-coverage','complexity']){
    $(id).addEventListener(id==='complexity'?'change':'input',render);
  }
  for(const el of document.querySelectorAll('.control-input'))el.addEventListener('change',render);
  for(const id of ['impact-volume','impact-retry-cost','impact-target-retry','impact-hourly','impact-hours-before','impact-hours-after'])
    $(id).addEventListener('input',renderImpact);
  $('impact-reset').addEventListener('click',()=>{resetImpact();msg('Economic assumptions reset to invented example values.')});
  $('impact-apply').addEventListener('click',()=>{
    const relevant=['benchmark','incident','governance'];
    for(const item of document.querySelectorAll('.control-input'))if(relevant.includes(item.value))item.checked=true;
    const unlinked=incidents.find(x=>!x.prevention);
    if(unlinked){unlinked.prevention='Targeted regression test proposed';unlinked.investigation='Control pending validation';}
    render();msg('Proposed prevention plan recorded. The displayed value remains hypothetical and depends on your assumed target, not on selecting controls.');
    $('impact-total').scrollIntoView({behavior:'smooth',block:'center'});
  });
  $('incident-form').addEventListener('submit',e=>{
    e.preventDefault();const title=$('incident-title-input').value.trim();if(!title)return;
    incidents.push({id:++serial,title,signal:$('incident-signal').value,severity:$('incident-severity').value,investigation:'Not investigated',prevention:''});
    $('incident-form').reset();render();msg('A synthetic incident was added.');
  });
  $('decision-form').addEventListener('submit',e=>{
    e.preventDefault();const owner=$('decision-owner').value.trim(),rationale=$('decision-rationale').value.trim();
    if(!owner||rationale.length<10){msg('Enter the reviewer and at least ten characters of rationale.');return;}
    const labels={hold:'Hold for validation',mitigate:'Mitigation required',exception:'Proposed exception'};
    const tier=scoreRisk(snapshot(),w()).tier;
    audit.push({owner,rationale,choice:labels[$('decision-choice').value],tier,time:new Date().toLocaleString()});
    $('decision-rationale').value='';$('decision-choice').value='hold';
    render();msg('Recorded a synthetic decision. No software was authorized for release.');
  });
  $('reset-demo').addEventListener('click',()=>{
    $('workflow').value='coaching';$('scenario').value='regression';
    document.querySelectorAll('.control-input').forEach(x=>x.checked=false);
    resetCandidate(true);resetImpact();$('workbench').scrollIntoView({behavior:'smooth'});
    msg('All synthetic examples reset.');
  });
  $('export-demo').addEventListener('click',()=>{
    const inputs=snapshot(),baseline=w(),risk=scoreRisk(inputs,baseline);
    const impactArgs=Object.fromEntries(['impact-volume','impact-retry-cost','impact-target-retry','impact-hourly','impact-hours-before','impact-hours-after'].map(id=>[id,n(id)]));
    const payload={notice:'SYNTHETIC PRI EDUCATIONAL SCENARIO. Not customer data, validated prediction, verified savings, or deployment evidence.',
      date:new Date().toISOString(),workflow:baseline.name,baseline:{p95:baseline.p95,unit:baseline.unit,success:baseline.success,retry:baseline.retry,cost:baseline.cost},
      candidate:inputs,transparentRisk:risk,incidentHistory:incidents,proposedControls:[...document.querySelectorAll('.control-input')].filter(x=>x.checked).map(x=>x.value),
      decisionLog:audit,impactModelAssumptions:impactArgs,
      limitations:['Impact assumes marginal cost per retry and sustained difference in rates.','Remediation hours represent capacity, not necessarily cash savings.','This does not establish causality or actual avoided incidents.','All workflow and incident data are synthetic.']};
    const file=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});
    const url=URL.createObjectURL(file),a=document.createElement('a');
    a.href=url;a.download='pri-synthetic-evidence.json';document.body.appendChild(a);a.click();a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1500);msg('Synthetic evidence snapshot exported.');
  });
  const mobile=$('.menu-button'),nav=$('sandbox-navigation');
  mobile.addEventListener('click',()=>{const open=mobile.getAttribute('aria-expanded')!=='true';mobile.setAttribute('aria-expanded',String(open));nav.classList.toggle('is-open',open)});
  nav.addEventListener('click',()=>{mobile.setAttribute('aria-expanded','false');nav.classList.remove('is-open')});
  $('scenario').value='regression';resetCandidate(true);resetImpact();
})();
