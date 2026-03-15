import re
from typing import Any, Dict, List, Optional, Tuple


_NEGATION_WORDS = {"no", "not", "without", "deny", "denies", "denied"}


def _normalize_text(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"[^a-z0-9\s]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _stem_word(word: str) -> str:
    w = (word or "").strip().lower()
    if len(w) <= 3:
        return w
    for suffix in ("ing", "ed", "es", "s"):
        if w.endswith(suffix) and len(w) - len(suffix) >= 3:
            return w[: -len(suffix)]
    return w


def _tokenize(text: str) -> List[str]:
    return [_stem_word(t) for t in _normalize_text(text).split() if t.strip()]


def _is_negated(tokens: List[str], start_index: int) -> bool:
    window = tokens[max(0, start_index - 2) : start_index]
    return any(t in _NEGATION_WORDS for t in window)


def _phrase_present(text: str, phrase: str) -> bool:
    phrase = (phrase or "").strip()
    if not phrase:
        return False

    text_tokens = _tokenize(text)
    phrase_tokens = _tokenize(phrase)
    if not text_tokens or not phrase_tokens:
        return False

    if len(phrase_tokens) == 1:
        target = phrase_tokens[0]
        for i, tok in enumerate(text_tokens):
            if tok == target and not _is_negated(text_tokens, i):
                return True
        return False

    # Contiguous multi-token phrase match
    n = len(phrase_tokens)
    for i in range(0, len(text_tokens) - n + 1):
        if text_tokens[i : i + n] == phrase_tokens and not _is_negated(text_tokens, i):
            return True
    return False


def _get_match_lists(rule: Dict[str, Any]) -> Tuple[List[str], List[str], List[str]]:
    match = rule.get("match") or {}
    all_list = match.get("all") or []
    any_list = match.get("any") or []
    none_list = match.get("none") or []

    if not isinstance(all_list, list):
        all_list = []
    if not isinstance(any_list, list):
        any_list = []
    if not isinstance(none_list, list):
        none_list = []

    all_list = [str(x) for x in all_list if str(x).strip()]
    any_list = [str(x) for x in any_list if str(x).strip()]
    none_list = [str(x) for x in none_list if str(x).strip()]

    return all_list, any_list, none_list


def rule_matches(text: str, rule: Dict[str, Any]) -> Tuple[bool, int]:
    all_list, any_list, none_list = _get_match_lists(rule)

    # 'none' must not appear
    for phrase in none_list:
        if _phrase_present(text, phrase):
            return False, 0

    # 'all' must appear
    for phrase in all_list:
        if not _phrase_present(text, phrase):
            return False, 0

    # 'any' (if provided) needs at least one
    any_hits = 0
    if any_list:
        any_hits = sum(1 for phrase in any_list if _phrase_present(text, phrase))
        if any_hits == 0:
            return False, 0

    score = (len(all_list) * 3) + any_hits
    return True, score


def pick_best_rule(message: str, rules: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    text = _normalize_text(message)

    best: Optional[Dict[str, Any]] = None
    best_score = -1
    best_priority = -10_000
    fallback: Optional[Dict[str, Any]] = None

    for rule in rules:
        if not isinstance(rule, dict):
            continue
        all_list, any_list, none_list = _get_match_lists(rule)
        if not all_list and not any_list and not none_list:
            # Treat "no criteria" as a fallback rule; only use if nothing else matches.
            if fallback is None:
                fallback = rule
            continue

        ok, score = rule_matches(text, rule)
        if not ok:
            continue

        try:
            priority = int(rule.get("priority", 0))
        except Exception:
            priority = 0

        # Prefer higher score; tie-breaker: more 'all' phrases (more specific).
        if priority > best_priority:
            best = rule
            best_score = score
            best_priority = priority
        elif priority == best_priority and score > best_score:
            best = rule
            best_score = score
        elif priority == best_priority and score == best_score and best is not None:
            best_all, _, _ = _get_match_lists(best)
            rule_all, _, _ = _get_match_lists(rule)
            if len(rule_all) > len(best_all):
                best = rule
                best_score = score

    return best or fallback
