// Scheduled by GitHub Actions. No responses or credentials are logged or checked in.
const {readResponses}=require('../services/lux-api/lib/lux-store');
const {due,summary}=require('../lib/lux-summary');
async function main(){
  if(!due()&&process.env.FORCE_DIGEST!=='true'){console.log('Not a digest day.');return;}
  const token=process.env.JJOPS_SLACK_BOT_TOKEN, recipient=process.env.JJOPS_USER_ID;
  if(!token||!recipient)throw Error('DM delivery is not configured');
  const records=await readResponses();
  const text=summary(records).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  const response=await fetch('https://slack.com/api/chat.postMessage',{method:'POST',headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},body:JSON.stringify({channel:recipient,text,mrkdwn:false,unfurl_links:false,unfurl_media:false}),signal:AbortSignal.timeout(15000)});
  const result=await response.json();if(!response.ok||!result.ok)throw Error('Slack delivery failed: '+(result.error||response.status));
  console.log('Digest delivered.');
}
main().catch(()=>{console.error('Lux digest failed. Check private storage and Slack configuration.');process.exitCode=1;});
