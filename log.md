# Log

**Time:** HUMAN: 30 to 45 minutes (reading, checking, deciding what ships). AI: about 2 hours of wall-clock time (Claude Code ran up to 7 agents at once, 15 in total, plus about 20 short fresh test sessions for C2).

**First instruction:** "stigo case study!!!" (Serbian for "the case study arrived!!!"). Claude Code found the zip on my Desktop, read the brief and the brain, drafted every answer with parallel agents, then ran review passes. I read, checked and decided what ships.

**Three things it got wrong**

1. **The first skill rewrite invented links and left vague dates.** In fresh reruns it called the product-page size chart issue "related to" an older size-chart item, which the call never said, and kept "by Wednesday" and "on Friday" in a summary. Caught by running each skill version in five fresh sessions and comparing the outputs. Fixed the instruction: two lines in the skill.
2. **A recap told the client something private happened.** The first 22 Sep recap said something was held back "after Dana left the call", and the checker the AI wrote had an exemption that let it pass. Caught by a review pass that read every line as Dana would. Fixed the output (the flag) and the tool (no exemption).
3. **It overstated a result.** It reported that the old skill, rerun with the brain, produced a clean recap. That run's flag also said the cut text came "after Theo left". Caught by rerunning the stricter checker over every saved run. Fixed only the output (the C2 table): the claim was wrong, not the skill.
