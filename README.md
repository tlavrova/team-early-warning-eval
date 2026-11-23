# Team Early Warning — Eval Project

A small LLM app that reads signals from a software team and warns early when
something is going wrong, plus a DeepEval test suite that checks whether those
warnings are any good.

Built as practice for the Udemy course
*Testing AI Systems with DeepEval: AI Agents, Chatbots & RAG*.

## 1. Problem

Team risks are usually visible days before they hurt, but nobody connects the
dots in time. The app should catch things like:

- **Sprint at risk:** too much work still open close to the sprint end
- **Blocked work:** someone waiting on another person, team or access
- **Overload:** one person holding far more work than others
- **Silent tickets:** tickets with no updates for several days

## 2. Input

A plain-text or JSON snapshot of the team, for example:

- Ticket list: title, assignee, status, last updated, days left in sprint
- Recent standup notes (free text, one entry per person per day)

## 3. Output

A short structured warning:

- `risk_level`: `low` | `medium` | `high`
- `reason`: one or two sentences, based only on the input
- `suggested_action`: one concrete next step

The warning must describe *situations*, not blame *people*.

## 4. Example

**Situation**

> Sprint ends in 2 days. 3 of 5 tickets are still "In Progress".
> Ana wrote "waiting on API access" in her last 3 standups.

**A good warning**

> `risk_level`: high
> `reason`: Most sprint work is unfinished with 2 days left, and one ticket has
> been blocked on API access for 3 days.
> `suggested_action`: Escalate the API access request today and agree which
> tickets move to the next sprint.

**Different wordings that are both correct**

- "High risk: 60% of tickets are open 2 days before the deadline, and API
  access has blocked work since Monday."
- "The sprint will likely slip. A blocker on API access has lasted three days.
  Unblock it now or reduce scope."

The wording differs, but the meaning matches: high risk, the same two reasons
and a sensible action. That is why the tests can't use an exact string match
(`output == expected`). DeepEval instead uses an LLM as a judge to score
qualities such as relevance, faithfulness to the input and usefulness.

## 5. How we'll evaluate it

| What we check | How (planned) |
|---|---|
| Warning is relevant to the input | Answer Relevancy metric |
| Reason is grounded in the data, nothing invented | Faithfulness / G-Eval |
| Suggested action is concrete and useful | Custom G-Eval metric |
| No blaming or biased language about people | Safety metrics (bias, toxicity) |
| Doesn't leak private team info | Red teaming (DeepTeam) |

Test cases will live in a Golden dataset of team scenarios with expected
outcomes.
