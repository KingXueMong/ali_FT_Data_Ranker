# README

## 目录

1. [说明](#说明)
   - [数据文件](#数据文件)
   - [数据处理代码](#数据处理代码)
   - [模型文件](#模型文件)
   - [模型训练代码](#模型训练代码)
2. [主要思路](#主要思路)

## 说明

本章节介绍关键文件及其存放路径.

### 数据文件

数据文件存放在data目录下。

### 数据处理代码

因为包含自定义算子，我便将所有文件打包一起上传。
数据配置文件存放路径为：`competition_kitproc_data/data-juicer/configs/data_juicer_recipes/alpaca_cot/alpaca-cot-en-refine.yaml`

其内容为：

```yaml
# global parameters
project_name: 'Data-Juicer-recipes-alpaca-cot-en'
dataset_path: '../data/raw_data/raw_data_en.jsonl'  # path to your dataset directory or file
export_path: '../data/proc_data/proc_data_en.jsonl'

np: 72  # number of subprocess to process your dataset
open_tracer: true

# process schedule
# a list of several process operators with their arguments
process:


  - clean_email_mapper:                                     # remove emails from text.
  - punctuation_normalization_mapper:                       # normalize unicode punctuations to English punctuations.
  - fix_unicode_mapper:                                     # fix unicode errors in text.
  - whitespace_normalization_mapper:

  - alphanumeric_filter: # 104636381
      tokenization: false
      min_ratio: 0.1
      max_ratio: 0.9
  - character_repetition_filter: # 104630030
      rep_len: 10
      max_ratio: 0.6
  - flagged_words_filter: # 104576967
      lang: en
      tokenization: true
      max_ratio: 0.017
  - maximum_line_length_filter: # 104575811
      min_len: 20
  - text_length_filter: # 104573711
      min_len: 20
      max_len: 10000
  - perplexity_filter:          # filter text with perplexity score out of specific range
      lang: en                                                # compute perplexity in what language
      max_ppl: 1000                                           # the max perplexity score to filter text
  - special_characters_filter:                              # filter text with special-char ratio out of specific range
      min_ratio: 0.0                                          # the min ratio of filter range
      max_ratio: 0.25
  - html_filter:

  - document_deduplicator: # 104636705
      lowercase: true
      ignore_non_character: true
  - document_simhash_deduplicator:  # 72855345
      tokenization: space
      window_size: 6
      lowercase: true
      ignore_pattern: '\p{P}'
      num_blocks: 9
      hamming_distance: 7

  - balanced_selector:

```

其中绝大多数都是内置算子，balanced_selector和html_filter为自定义算子。其实现代码位于`competition_kit/proc_data/data-juicer/data_juicer/ops/selector/balanced_selector.py`。

### 模型文件

训练后的模型文件位于`competition_kit/proc_data/falcon-rw-1b_output`目录下。



## 主要思路

主要思路以过滤优质数据集为主，使用常规的内置mapper以及filter，通过手工对比数据发现，英文数据集来源为17个数据集类别，我们发现在过滤完数据之后，各个数据集的数量差别较大，最多的数据集和最低的数据集数量相差百倍，我们通过自定义选择器，控制最多的数据集和最低的数据集数量相差不会超过5倍（完全平衡token数量达不到3M），使得其数据集相对平衡。
其中某些数据集中包含了对代码的理解文本，为提高测试集效果（测试集以文本理解为主要），将包含html代码的文本删去。

### 手写算子 

html_filter。该算子过滤了包含html代码的text。

balanced_selector。该算子功能为平衡数据集，是的数据集数量不会超过5倍。

