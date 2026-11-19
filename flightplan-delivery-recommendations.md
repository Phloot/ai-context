# Flightplan Delivery: Software Factory Recommendations

*November 19, 2026*

Flightplan’s Delivery workflow takes an Agility story through planning, critique by a second model family, human plan approval, slice execution and review, and final acceptance. The first change I’d make is to define **what evidence lets a story move through those stages**. The planner, critic, executor, and reviewers can all agree while sharing the same mistaken interpretation of an acceptance criterion. Decide early how a developer could observe the intended behavior, then run that check against the combined change.

GitHub Spec Kit already offers specification, planning, task generation, and cross-artifact analysis. Flightplan’s opportunity is to connect those activities to the developer’s Agility story, codebase, IntelliJ workflow, Jenkins builds, and internal engineering practices. A developer should be able to open a completed run and answer three questions in under a minute: **What changed? What proves it works? What still needs my judgment?** [1][ref-1]

## 1. Give each reviewer a different decision

Some overlap between plan critique and implementation review is appropriate, especially around compatibility and scope. Give each stage a distinct job so developers can see what the extra review bought them.

| Stage | Decision it owns | What it should return |
|---|---|---|
| Plan critique | Is this the right behavior, and is the approach justified by the repo? | A missed caller, an unsupported assumption, a simpler existing mechanism, a missing dependency, or a product decision someone must make. |
| Human plan review | Are the proposed behavior and tradeoffs acceptable? | A short view of decisions, assumptions, and scope changes. Put the full plan and slice details one click deeper. |
| Slice review | Does this diff work through its normal entry point and preserve the behavior existing callers rely on? | Findings tied to a changed location, an affected caller or scenario, and the consequence. Separate blockers from suggestions. |
| Final acceptance | Does the integrated change satisfy the original story and approved clarifications? | A result for each criterion, with evidence from the integrated revision and an explicit status for anything that still needs CI or human judgment. |

**Keep the opposite-family critic and measure its value.** Give it the original story and access to the repo. Have it form an initial view of the risky assumptions before showing it the planner’s rationale. That gives you a second interpretation as well as a second model. In SWE-PRBench, a study of 350 open-source pull requests, eight models caught 15–31% of human-flagged issues when reviewing only the diff. That figure is specific to the benchmark. Evaluate what Flightplan’s reviewers catch on your own repositories. [2][ref-2]

## 2. Design acceptance during planning and run it during delivery

For each material acceptance criterion, have the planner record **the observable outcome, the cheapest credible way to verify it, and where that check can run**. Reuse an existing test when it covers the behavior. A bug fix might warrant a regression test that fails on the base revision. A performance claim might need a baseline measurement. A staging-only behavior should remain visibly unverified until staging evidence exists.

Consider a story that says *a second team cannot reserve staging while another team holds it*. An executor could implement a read-before-write check. A reviewer could inspect the branch, see a passing test for an existing reservation, and reasonably approve it. Two simultaneous requests could still both succeed. The plan critic’s most valuable contribution here is one concrete question: **Does the guarantee also apply when both teams request an available environment at the same time?** If yes, submit concurrent requests through the reservation entry point and verify that exactly one acquires the reservation.

For important behaviors like that one, let the developer see and approve the scenario before execution. Flag changes to its expected outcome during implementation. StrongDM describes keeping some end-to-end scenarios outside the codebase as an independent check. Flightplan could borrow that idea selectively for shared contracts and recurring regressions. Anthropic’s evaluation guidance recommends deterministic grading where possible and explicit uncertainty where evidence is insufficient. [3][ref-3], [4][ref-4]

## 3. Integrate accepted slices early and bound the repair loops

Two individually correct slices can disagree about a payload, configuration default, migration order, or retry guarantee without touching the same file. **Make an integrated story branch part of execution.** The final acceptance node can then review a revision that has already received feedback along the way.

- Prefer slices that deliver a thin, testable behavior. When a plan splits work into persistence, service, and API layers, ask whether an early slice can exercise one path through all three.
- Give parallel slices separate worktrees. As each lands on the story branch, run the relevant checks against the combined revision. If a fix changes a shared contract, revisit the dependent slices and their evidence.
- Route failures by cause. An implementation defect goes to the executor. An invalid design assumption goes to the planner. An ambiguous requirement goes to the developer. An unavailable Artifactory dependency or Jenkins agent gets an infrastructure status. Sending all four to the executor invites unrelated code changes.
- Stop a repair loop when the same finding returns without new evidence. Show the developer the competing interpretations, attempted fix, and failing check so they can resolve it directly.

DORA identifies regrouping small batches before downstream testing as a pitfall. Stripe’s Minions provide a concrete precedent for bounded retries. Deterministic local checks run before CI, and after a second CI run the branch returns to a human. For Flightplan, set limits according to the cost of the check and whether the next attempt has a new hypothesis. [5][ref-5], [6][ref-6]

## 4. Make local development the product advantage

| Capability | What a developer should be able to do |
|---|---|
| Preflight before execution | See whether the repo can build locally, which checks require Jenkins, and whether a missing JDK, Docker runtime, VPN connection, or artifact credential will block the run. |
| Take over in IntelliJ and resume | Pause a slice, open its exact worktree, edit the code, and resume review from that diff. After a laptop restart, recover the last completed step. If a Jenkins build was already submitted, reconnect to that build by ID. |
| Reviewable handoff | Open the story-level diff, acceptance evidence, unresolved risks, and exact commands to reproduce a result. Follow a link to the Jenkins build for the reviewed commit. Open the agent transcript when debugging requires it. |
| Scoped local execution | See which files, commands, and integrations each role can access. Worktrees isolate parallel edits. Shell credentials, network access, and remote MCP actions need their own controls. Reading a Jenkins log and triggering a deployment are materially different capabilities. [6][ref-6], [7][ref-7] |
| Shorter path for small work | Take a reproducible, single-service bug from reproduction to a focused fix and review. A shared Jenkins library change may justify the full plan, downstream caller analysis, and compatibility checks. Let developers see and change the proposed route. |

**Prioritize takeover and resume.** A developer who spots a five-line correction halfway through a run should be able to make it in IntelliJ and hand the slice back. If their options are to explain the edit to an agent or abandon the run, Flightplan adds friction precisely when the developer knows the answer.

## 5. Evaluate Flightplan on your own historical stories

Uber describes evaluating its review agent against real internal PRs with known bugs, measuring precision, recall, cost, latency, and noise. That practice gives Flightplan a way to decide whether a second model family, another review pass, or a particular skill earns its place. [8][ref-8]

Start with a small set of historical Agility stories and their **pre-change** repo revisions. Include ordinary successes, bugs that escaped review, changes with downstream callers, and at least one story where asking a human was the correct outcome. Keep the eventual fix and known findings out of the agents’ inputs. Compare the full workflow with a simpler executor-plus-checks baseline on those same stories.

| Pilot metric | What to record |
|---|---|
| Developer effort | Active minutes spent clarifying, reviewing, and correcting a story through PR readiness. Record elapsed time separately. |
| Review value | Known defects caught, valid new findings, false blockers, and which stage first discovered each issue. |
| Delivery quality | Stories marked accepted that later fail relevant CI, require substantive human rework, or produce a regression. |
| Economics | Model usage, CI minutes, and repair attempts per accepted story, broken down by change type. |

## Recommended build order

1. **Criterion-level evidence and an integrated story branch.** Let developers inspect what demonstrates each behavior on the combined revision. Start collecting pilot metrics here.
2. **Local takeover and recovery.** Let developers correct a slice directly and resume the run from their change.
3. **Historical replay.** Use the results to tune reviewers, model selection, and workflow routing.

## References

1. GitHub, [Spec Kit documentation](https://github.github.com/spec-kit/). Overview of spec-driven development, planning, task generation, and cross-artifact analysis.
2. Deepak Kumar, [SWE-PRBench: Benchmarking AI Code Review Quality Against Pull Request Feedback](https://arxiv.org/abs/2603.26130). Research preprint describing the 350-PR benchmark, its review configurations, and issue detection results.
3. StrongDM, [Software Factory](https://factory.strongdm.ai/). Firsthand account of using end-to-end scenarios held outside the implementation codebase.
4. Anthropic, [Demystifying evals for AI agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents). Guidance on outcomes, deterministic graders, model judgment, uncertainty, and regression evaluation.
5. DORA, [Working in small batches](https://dora.dev/capabilities/working-in-small-batches/). Guidance on slicing changes and the cost of delaying downstream feedback.
6. Stripe, [Minions: Stripe’s one-shot, end-to-end coding agents, Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2). Engineering account of isolated development environments, deterministic workflow steps, local checks, and bounded CI repair.
7. GitHub, [Understanding filesystem policies for local sandboxing in GitHub Copilot CLI](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/understanding-local-sandboxing). Documents how enforcement differs across shell processes, built-in tools, and local and remote MCP servers.
8. Uber Engineering, [Running a Software Factory Efficiently at Uber Scale](https://www.uber.com/us/en/blog/efficient-software-factory/). Describes benchmarking code review on real PRs with known bugs and tracking quality, noise, latency, and cost per review.

[ref-1]: https://github.github.com/spec-kit/
[ref-2]: https://arxiv.org/abs/2603.26130
[ref-3]: https://factory.strongdm.ai/
[ref-4]: https://www.anthropic.com/research/demystifying-evals-for-ai-agents
[ref-5]: https://dora.dev/capabilities/working-in-small-batches/
[ref-6]: https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2
[ref-7]: https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/understanding-local-sandboxing
[ref-8]: https://www.uber.com/us/en/blog/efficient-software-factory/
