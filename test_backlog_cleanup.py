# ---
# title: test_backlog_cleanup
# description: 미병합 브랜치 병합과 오래된 카드 정리(TASK-42) 결과를 git 이력과 백로그 파일로 확인하는 테스트
# authors: [coralstay]
# license: AGPL-3.0-only
# status: draft
# task: TASK-42
# created_date: '2026-11-22'
# updated_date: '2026-11-22'
# ---
# TASK-42: 미병합 브랜치(task/TASK-4·25·20) 병합과 오래된 카드 정리
#
# The cleanup only moves history and backlog files, so these tests read the
# repository itself: the three branch tips must be ancestors of HEAD with the
# human Plan-Approved commits intact, closed cards must carry evidence notes,
# moved cards must sit in the archive, and the folded TASK-28 / DRAFT-14 must
# be byte-identical to before the cleanup.
import glob
import os
import re
import subprocess
import unittest

REPO = os.path.dirname(os.path.abspath(__file__))
# branch tips merged by TASK-42 (task/TASK-4 tip includes the TASK-42 card, its signature and In Progress)
TIPS = {
    "task/TASK-4": "4f9477b3c9e6d6ff88dcc7028520673b99afb4c5",
    "task/TASK-25": "4739a385d01ea0f4646fb79bce5771bf095b8044",
    "task/TASK-20": "625e3daaf354c5c08e2b8da2bddafd967b35982a",
}
CLOSED_WITH_EVIDENCE = ["TASK-4", "TASK-5", "TASK-6", "TASK-12", "TASK-13", "TASK-15", "TASK-24"]
MOVED_TO_UPKEEP = ["task-17", "task-18", "task-19", "task-20", "task-21", "task-22"]


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True, check=False)


def card_text(task_id, folder="backlog/tasks"):
    n = task_id.split("-")[1]
    paths = glob.glob(os.path.join(REPO, folder, f"task-{n} - *.md"))
    assert len(paths) == 1, (task_id, paths)
    with open(paths[0], encoding="utf-8") as f:
        return f.read()


def status(text):
    return re.search(r"^status: (.+)$", text, re.MULTILINE).group(1).strip()


# == AC/DoD ==


class TestBranchesMerged(unittest.TestCase):
    def test_tips_are_ancestors_of_head(self) -> None:
        """TASK-42#1 TASK-42#B2: each branch was merged (not rebased): its own tip commit is in HEAD's history."""
        for name, tip in TIPS.items():
            with self.subTest(branch=name):
                self.assertEqual(git("merge-base", "--is-ancestor", tip, "HEAD").returncode, 0)

    def test_plan_approved_commits_survive(self) -> None:
        """TASK-42#1 TASK-42#B2: the Plan-Approved commits of the round-2 cards and of TASK-42 are reachable unchanged."""
        subjects = set(git("log", "--format=%s", "HEAD").stdout.splitlines())
        for n in [*range(29, 35), *range(37, 42), 42]:  # TASK-35·36 were never approved
            with self.subTest(card=n):
                self.assertIn(f"Plan-Approved: TASK-{n}", subjects)


class TestCardsClassified(unittest.TestCase):
    def test_closed_cards_are_done_with_evidence(self) -> None:
        """TASK-42#2 TASK-42#B1: cards closed here are Done and their notes name the merged PR, lint and tests."""
        for task_id in CLOSED_WITH_EVIDENCE:
            with self.subTest(card=task_id):
                text = card_text(task_id)
                self.assertEqual(status(text), "Done")
                self.assertIn("병합 PR #", text)
                self.assertIn("lint --strict rc=0", text)
                self.assertIn("테스트·빌드:", text)

    def test_folded_work_is_untouched(self) -> None:
        """TASK-42#2 TASK-42#B3: TASK-28 and DRAFT-14 are byte-identical to before the cleanup."""
        before = TIPS["task/TASK-4"]
        for pattern in ("backlog/tasks/task-28 - *.md", "backlog/drafts/draft-14 - *.md"):
            with self.subTest(pattern=pattern):
                path = os.path.relpath(glob.glob(os.path.join(REPO, pattern))[0], REPO)
                self.assertEqual(git("diff", "--quiet", before, "HEAD", "--", path).returncode, 0)

    def test_cleanup_commits_touch_only_backlog(self) -> None:
        """TASK-42#2 TASK-42#B4: commits made for TASK-42 (not the merged branches) change backlog/ and this test file only."""
        log = git("log", "--no-merges", "--format=%H", f"{TIPS['task/TASK-4']}..HEAD", "--not",
                  TIPS["task/TASK-25"], TIPS["task/TASK-20"]).stdout.split()
        touched = set()
        for sha in log:
            touched.update(git("show", "--name-only", "--format=", sha).stdout.split("\n"))
        touched.discard("")
        self.assertTrue(touched)
        self.assertTrue(all(p.startswith("backlog/") or p == "test_backlog_cleanup.py" for p in touched), touched)


class TestMovedAndOwned(unittest.TestCase):
    def test_upkeep_cards_are_archived(self) -> None:
        """TASK-42#3: TASK-17~22 moved to upkeep live in the archive, not on the board."""
        for stem in MOVED_TO_UPKEEP:
            with self.subTest(card=stem):
                self.assertEqual(glob.glob(os.path.join(REPO, "backlog/tasks", f"{stem} - *.md")), [])
                self.assertEqual(len(glob.glob(os.path.join(REPO, "backlog/archive/tasks", f"{stem} - *.md"))), 1)

    def test_other_owners_are_noted(self) -> None:
        """TASK-42#3: cards owned by Antigravity or another Claude session say so."""
        self.assertIn("Antigravity 담당", card_text("TASK-35"))
        for task_id in ("TASK-14", "TASK-36"):
            with self.subTest(card=task_id):
                self.assertIn("다른 Claude 세션", card_text(task_id))


class TestVerifiedAndRecorded(unittest.TestCase):
    def test_lint_is_clean_after_the_merge(self) -> None:
        """TASK-42#4: source-header lint --strict passes on the merged tree."""
        tool = os.path.join(REPO, "source-header.py")
        result = subprocess.run(["python3", tool, "lint", "--strict", "."], cwd=REPO, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_notes_carry_table_outputs_and_pr(self) -> None:
        """TASK-42#D1 TASK-42#D2 TASK-42#D3: the card notes hold the classification table, the test/lint output and the PR."""
        text = card_text("TASK-42")
        self.assertIn("분류표", text)
        self.assertIn("passed", text)
        self.assertIn("PR", text)
        self.assertIn("task/TASK-42", text)  # PR source branch; the PR number is appended once it exists


# == Coverage ==


class TestHelpers(unittest.TestCase):
    def test_status_reads_frontmatter(self) -> None:
        self.assertEqual(status("---\nid: X\nstatus: Done\n---\n"), "Done")


if __name__ == "__main__":
    unittest.main()
