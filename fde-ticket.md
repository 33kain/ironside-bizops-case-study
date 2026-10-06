# Recap agent: privacy, speed, coverage

1. **Privacy in code, not the prompt.** Cut the transcript where the last client leaves, before the model sees it. Check every recap before posting ([check_recap.py](extra/check_recap.py) is a start); a FAIL goes to the AM.

   Evidence: a DM, read out after the client left, reached the client's channel ([bad-recap.md](workers/output/bad-recap.md), c084). Fresh runs of the same skill left it out ([1](workers/runs/0-old-skill-no-brain.md), [2](workers/runs/1-old-skill-with-brain.md)): a prompt can't guarantee it. Same risk in [call-1.md](inbox/call-1.md) after 01:44.

2. **Post within 15 min (p90).** Log each stage: no agent recap came under 45 min, likely a fixed wait.

   Evidence: agent median 65 min, AMs 18 min ([calls.csv](calls.csv)). On-time agent posts alone lift South from 35% to 85%. Its lead: "if it posted in 10-15 min I'd use it" ([slack](slack-thread.txt)).

3. **Cover non-Meet calls:** AM voice notes, WhatsApp or phone recordings.

   Evidence: 34 of 140 calls never reach the agent.
