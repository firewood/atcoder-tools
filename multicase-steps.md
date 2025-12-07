# AtCoder Tools Multiple Test Cases Implementation Plan

## 概要

この文書は、atcoder-toolsにおいて1つのファイルに複数のテストケースが含まれる問題に対応するための段階的な実装計画を記述します。

## 現状分析

### 現在の実装状況
- 現在のstableブランチは単一テストケースのみに対応
- chaemon/multi_testcase ブランチに包括的な実装が存在
- 主要な変更点：
  - ProblemContentクラスの input_format_text を文字列から文字列リストに変更
  - InputFormatクラスの追加
  - 複数入力形式の解析機能
  - コード生成での複数テストケース対応

### 対象問題タイプ
- 複数テストケースが1つのファイルにまとめられている問題
- 各テストケース毎に入力/出力形式が定義されている問題

## 段階的実装計画

### ステップ1: データ構造の拡張 (基盤整備)

**変更対象ファイル:**
- `atcodertools/client/models/problem_content.py`

**実装内容:**
1. InputFormatクラスの追加
   ```python
   class InputFormat:
       def __init__(self, input_format: list[str]):
           self.type = None
           self.loop_length_var = None
           self.input_format = input_format
   ```

2. ProblemContentクラスの修正
   - `input_format_text`を単一文字列から文字列リストに変更
   - `input_format_data`フィールドを追加
   - `get_input_format()`メソッドの戻り値型を修正

3. HTMLパース処理の更新
   - `_primary_strategy()`メソッドの修正：複数の`<pre>`タグを配列で取得
   - `normalize_soup()`関数の追加
   - `_strip_case_vars()`関数の追加（ケース変数の除去）

**テスト対象:**
- 既存の単一テストケース問題が正常動作すること
- 新しいデータ構造への適切な変換

### ステップ2: フォーマット予測の拡張

**変更対象ファイル:**
- `atcodertools/fmtprediction/predict_format.py`
- `atcodertools/fmtprediction/predict_simple_format.py`

**実装内容:**
1. `predict_format()`関数の修正
   - 戻り値を単一結果からリスト形式に変更
   - 複数入力形式に対応した予測ロジック

2. `suspect_single_string()`関数の追加
   - 単一文字列パターンの検出機能

3. 複数フォーマットの予測処理
   - 各フォーマットに対する独立した予測
   - フォーマット間の整合性チェック

**テスト対象:**
- 複数入力形式の正しい検出
- 既存単一形式との互換性

### ステップ3: コード生成の拡張

**変更対象ファイル:**
- `atcodertools/codegen/code_generators/universal_code_generator.py`
- テンプレートファイル群

**実装内容:**
1. UniversalCodeGeneratorクラスの修正
   - `_format`を配列として扱う修正
   - `_input_part_with_solve_function()`メソッドの追加
   - 複数テストケース用の入力部生成

2. テンプレート変数の拡張
   - `input_part_with_solve_function`: solve関数内での入力処理用
   - 既存テンプレート変数の互換性維持

3. 言語別テンプレートの更新
   - C++, D, その他の言語テンプレートでのmulticase対応

**テスト対象:**
- 複数テストケースでの正しいコード生成
- 各言語での動作確認

### ステップ4: テスト機能の拡張

**変更対象ファイル:**
- テスト関連のリソースファイル
- テスト実行ロジック

**実装内容:**
1. 複数テストケース用のテストデータ追加
   - `tests/resources/` 以下に multisolution テストケースを追加

2. テスターの動作確認
   - 複数テストケースでの正しい実行
   - 各テストケースの独立した検証

**テスト対象:**
- multisolutionテストケースでの正常動作
- 既存テストとの非回帰

### ステップ5: 統合テストと検証

**実装内容:**
1. 実際のAtCoderコンテスト問題での検証
   - 既知のmulticaseな問題でのテスト
   - 生成コードの動作確認

2. パフォーマンステスト
   - 大量テストケースでの動作確認
   - メモリ使用量の検証

3. エラーハンドリングの強化
   - 不正な入力形式の適切な処理
   - ユーザーフレンドリーなエラーメッセージ

## 実装上の注意事項

### 互換性の維持
- 既存の単一テストケース問題への影響を最小化
- APIの後方互換性を可能な限り維持
- 段階的なロールアウトによるリスク軽減

### エラーハンドリング
- 複数形式の解析失敗時のフォールバック処理
- 不明な形式に対する適切なエラー報告

### パフォーマンス考慮
- 大量テストケースでのメモリ効率
- 解析処理の最適化

## 検証方法

### 単体テスト
- 各ステップでの機能単位テスト
- 既存テストの非回帰確認

### 統合テスト
- 実際のAtCoder問題を使った検証
- 複数言語での動作確認

### ユーザビリティテスト
- 実際の開発フローでの使用感確認
- エラー時の分かりやすさ検証

## まとめ

この計画に沿って段階的に実装することで、リスクを最小化しながらmulticaseテストケース対応機能を安全に導入できます。各ステップでの十分なテストにより、既存機能への影響を防ぎつつ新機能を提供します。