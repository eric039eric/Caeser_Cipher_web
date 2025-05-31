#!/usr/bin/env python3
"""
Enhanced Caesar Cipher CLI
=========================
• Encrypt / Decrypt text interactively
• Custom shift (0–25)
• Handles whitespace & punctuation without errors
• Optional ⟨keep⟩ or ⟨encode⟩ punctuation/spaces
  – encode mode substitutes each punctuation with a fixed placeholder symbol
    so ciphertext中連標點都不易被識別（純好玩用途）

安全提醒：Caesar 加密極易破解，只適用於玩具或教學！
"""

import string
import sys
from typing import Callable

ABC = string.ascii_lowercase  # 基本字母表
PUNCT = string.punctuation    # 標點符號集合

# ──────────────────────────────────────────────────────────────
# Mapping  utilities
# ──────────────────────────────────────────────────────────────

def build_maps(shift: int, encode_punct: bool, encode_space: bool):
    """Return (enc_map, dec_map) dicts according to user prefs"""
    shift %= 26
    sub = ABC[shift:] + ABC[:shift]
    enc_map = {a: b for a, b in zip(ABC, sub)}

    # Extend maps for punctuation/space if user chose to encode them
    if encode_punct:
        # Use a simple reversible substitution: rotate punctuation list
        punct_sub = PUNCT[shift % len(PUNCT):] + PUNCT[: shift % len(PUNCT)]
        enc_map.update({p: q for p, q in zip(PUNCT, punct_sub)})
    if encode_space:
        enc_map[" "] = "\u2581"  # 替換成下底線方塊 ▁

    # decode map is inverse of enc_map
    dec_map = {v: k for k, v in enc_map.items()}
    return enc_map, dec_map


# ──────────────────────────────────────────────────────────────
# Transform logic
# ──────────────────────────────────────────────────────────────

def transform(text: str, mapping: dict[str, str]) -> str:
    res: list[str] = []
    for ch in text:
        # 英文字母 (大小寫)
        base = ch.lower()
        if base in mapping:
            mapped = mapping[base]
            # 保持原大小寫
            res.append(mapped.upper() if ch.isupper() else mapped)
        else:
            # 任何其他未映射字元 (例：中文字、數字、換行) -> 原樣
            res.append(ch)
    return "".join(res)


# ──────────────────────────────────────────────────────────────
# CLI helpers
# ──────────────────────────────────────────────────────────────

def prompt_int(msg: str, default: int, validate: Callable[[int], bool]):
    while True:
        raw = input(f"{msg} [{default}]: ").strip()
        if not raw:
            return default
        if raw.lstrip("-+ ").isdigit():
            val = int(raw)
            if validate(val):
                return val
        print("⚠️  必須輸入有效整數，請重試！")


def prompt_yn(msg: str, default: bool) -> bool:
    dv = "Y" if default else "n"
    raw = input(f"{msg} (Y/n) [{dv}]: ").strip().lower()
    if not raw:
        return default
    return raw.startswith("y")


# ──────────────────────────────────────────────────────────────
# Main loop
# ──────────────────────────────────────────────────────────────

def main():
    print("\n=== Caesar Cipher CLI (Enhanced) ===\n")
    while True:
        mode = input("選擇模式 (E)ncrypt / (D)ecrypt / (Q)uit: ").strip().lower()
        if mode == "q":
            print("Bye!")
            break
        if mode not in ("e", "d"):
            print("⚠️  請輸入 E、D 或 Q。\n")
            continue

        shift = prompt_int("請輸入位移量 0–25", 3, lambda x: 0 <= x <= 25)
        encode_punct = prompt_yn("是否連標點符號一起編碼?", False)
        encode_space = prompt_yn("是否連空白(空格)一起編碼?", False)

        enc_map, dec_map = build_maps(shift, encode_punct, encode_space)
        mapping = enc_map if mode == "e" else dec_map

        print("\n貼上/輸入文字，完畢後按 Enter → Ctrl+D (Mac/Linux) 或 Ctrl+Z Enter (Windows) 結束輸入:\n")
        try:
            raw_text = sys.stdin.read()
        except KeyboardInterrupt:
            print("\n⚠️  已取消\n")
            continue
        if not raw_text.strip():
            print("⚠️  沒收到文字，請重試！\n")
            continue

        result = transform(raw_text, mapping)
        print("\n=== 轉換結果 ===")
        print(result)
        print("\n================\n")

        # 再次？
        if not prompt_yn("是否繼續", True):
            print("Bye!")
            break


if __name__ == "__main__":
    main()
